# transport_spare_parts_milp.py
import pulp
import time
import io
import sys
from tabulate import tabulate

# ---------------------------
# Data
# ---------------------------
Bases = ["Delhi", "Mumbai", "Bengaluru"]
Stations = ["Kolkata", "Hyderabad", "Chennai"]
Parts = ["P1", "P2"]
Periods = [1, 2, 3]

# initial inventory at bases [base][part]
init_inv = {
    ("Delhi", "P1"): 10, ("Delhi", "P2"): 5,
    ("Mumbai", "P1"): 8, ("Mumbai", "P2"): 8,
    ("Bengaluru", "P1"): 5, ("Bengaluru", "P2"): 10,
}

# demand[period][station][part]
demand = {
    1: { "Kolkata": {"P1": 8,  "P2": 6},
         "Hyderabad": {"P1": 12, "P2": 10},
         "Chennai": {"P1": 10, "P2": 12}},
    2: { "Kolkata": {"P1": 10, "P2": 8},
         "Hyderabad": {"P1": 11, "P2": 11},
         "Chennai": {"P1": 12, "P2": 9}},
    3: { "Kolkata": {"P1": 9,  "P2": 10},
         "Hyderabad": {"P1": 13, "P2": 12},
         "Chennai": {"P1": 11, "P2": 13}},
}

# transport costs per unit (₹ thousands) by mode
truck_cost = { # cheaper
    ("Delhi","Kolkata"): 1.8, ("Delhi","Hyderabad"): 2.0, ("Delhi","Chennai"): 2.2,
    ("Mumbai","Kolkata"): 2.1, ("Mumbai","Hyderabad"): 1.9, ("Mumbai","Chennai"): 2.0,
    ("Bengaluru","Kolkata"): 2.6, ("Bengaluru","Hyderabad"): 1.8, ("Bengaluru","Chennai"): 1.6,
}
air_cost = { # expensive, fast
    k: v + 1.5 for k,v in truck_cost.items()
}

# truck capacity per base per period (shared across parts/stations)
truck_capacity = {"Delhi": 25, "Mumbai": 20, "Bengaluru": 18}

# purchase (external supplier) unit cost per part (₹k/unit)
purchase_cost = {"P1": 5.0, "P2": 7.0}
fixed_order_cost = 50.0  # ₹k per base-period if any order placed

# holding cost per unit per period (₹k)
holding_cost = {"P1": 0.2, "P2": 0.25}

# shortage penalty per unit (₹k)
shortage_cost = {"P1": 20.0, "P2": 25.0}

# repair return fraction (a fraction of units consumed that return next period to bases)
repair_return = {"P1": 0.20, "P2": 0.10}

# Big-M for linking binary order variable
BIGM = 1e6

# ---------------------------
# Model
# ---------------------------
model = pulp.LpProblem("Aerospace_Spare_Parts_MILP", pulp.LpMinimize)

# Decision variables:
# order_qty[base,part,period]  (ordered from supplier, arrives next period)
order_qty = pulp.LpVariable.dicts("OrderQty",
                                  ((b,p,t) for b in Bases for p in Parts for t in Periods),
                                  lowBound=0, cat="Continuous")

# y_order[b,t] binary whether an order is placed at base b in period t
y_order = pulp.LpVariable.dicts("Y_Order",
                                ((b,t) for b in Bases for t in Periods),
                                lowBound=0, upBound=1, cat="Binary")

# ship_truck[b,s,p,t] quantity shipped by truck from base b to station s for part p in period t
ship_truck = pulp.LpVariable.dicts("ShipTruck",
                                   ((b,s,p,t) for b in Bases for s in Stations for p in Parts for t in Periods),
                                   lowBound=0, cat="Continuous")

# ship_air[b,s,p,t] quantity shipped by air (no capacity)
ship_air = pulp.LpVariable.dicts("ShipAir",
                                 ((b,s,p,t) for b in Bases for s in Stations for p in Parts for t in Periods),
                                 lowBound=0, cat="Continuous")

# inventory[b,p,t] inventory at base b for part p at end of period t
inventory = pulp.LpVariable.dicts("Inv",
                                  ((b,p,t) for b in Bases for p in Parts for t in Periods),
                                  lowBound=0, cat="Continuous")

# shortage (backorder) at station s for part p at period t (units unmet; penalized)
shortage = pulp.LpVariable.dicts("Shortage",
                                 ((s,p,t) for s in Stations for p in Parts for t in Periods),
                                 lowBound=0, cat="Continuous")

# consumed[s,p,t] amount consumed at station s for part p at t (satisfies up to demand)
# For bookkeeping we can compute consumed = demand - shortage, but keep variable for clarity
consumed = pulp.LpVariable.dicts("Consumed",
                                 ((s,p,t) for s in Stations for p in Parts for t in Periods),
                                 lowBound=0, cat="Continuous")

# ---------------------------
# Objective: minimize total cost
# ---------------------------
transport_cost = pulp.lpSum([truck_cost[(b,s)] * ship_truck[(b,s,p,t)]
                             + air_cost[(b,s)] * ship_air[(b,s,p,t)]
                             for b in Bases for s in Stations for p in Parts for t in Periods])

purchase_cost_total = pulp.lpSum([purchase_cost[p] * order_qty[(b,p,t)]
                                 for b in Bases for p in Parts for t in Periods])

fixed_order_total = pulp.lpSum([fixed_order_cost * y_order[(b,t)] for b in Bases for t in Periods])

holding_cost_total = pulp.lpSum([holding_cost[p] * inventory[(b,p,t)]
                                for b in Bases for p in Parts for t in Periods])

shortage_cost_total = pulp.lpSum([shortage_cost[p] * shortage[(s,p,t)]
                                 for s in Stations for p in Parts for t in Periods])

model += (transport_cost + purchase_cost_total + fixed_order_total +
          holding_cost_total + shortage_cost_total), "Total_Cost"

# ---------------------------
# Constraints
# ---------------------------

# 1) Linking order binary and order qty: if order_qty > 0 => y_order =1
for b in Bases:
    for t in Periods:
        model += pulp.lpSum([order_qty[(b,p,t)] for p in Parts]) <= BIGM * y_order[(b,t)], f"OrderLink_{b}_{t}"

# 2) Truck capacity per base per period (sum across ships by truck, all parts & stations)
for b in Bases:
    for t in Periods:
        model += pulp.lpSum([ship_truck[(b,s,p,t)] for s in Stations for p in Parts]) <= truck_capacity[b], f"TruckCap_{b}_{t}"

# 3) Inventory balance at bases
# Note: orders placed in t arrive in t+1, so for t=1 initial inventory + arrivals from orders at t-1 (none) + returns from consumption in t-1 (none).
# We model for each t:
for b in Bases:
    for p in Parts:
        for t in Periods:
            # arrivals from orders placed in t-1 -> arrive in t
            arrivals = order_qty[(b,p,t-1)] if t-1 >= 1 else 0
            # returns from repairs: sum over stations consumed in t-1 * return fraction distributed equally (for simplicity assume returns go to same base proportionally)
            # To keep things linear and simple, assume returns are aggregated back to bases in proportion to initial inventory share
            # Compute fraction share of base b for that part:
            total_init = sum(init_inv.get((bb,p), 0) for bb in Bases)
            if total_init <= 0:
                base_share = 1.0 / len(Bases)
            else:
                base_share = init_inv.get((b,p), 0) / total_init

            # returns amount to base b in period t = base_share * sum_s consumed[s,p,t-1] * repair_return[p]
            if t-1 >= 1:
                returns = repair_return[p] * base_share * pulp.lpSum([consumed[(s,p,t-1)] for s in Stations])
            else:
                returns = 0

            # outflows from base in period t: shipments by truck + air
            outflows = pulp.lpSum([ship_truck[(b,s,p,t)] + ship_air[(b,s,p,t)] for s in Stations])

            # inventory balance:
            if t == 1:
                model += (init_inv.get((b,p), 0) + arrivals + returns - outflows == inventory[(b,p,t)]), f"InvBal_{b}_{p}_{t}"
            else:
                # inventory_{t-1} + arrivals + returns - outflows = inventory_t
                model += (inventory[(b,p,t-1)] + arrivals + returns - outflows == inventory[(b,p,t)]), f"InvBal_{b}_{p}_{t}"

# 4) Consumption and shortage relation at stations: consumed + shortage = demand
for t in Periods:
    for s in Stations:
        for p in Parts:
            model += consumed[(s,p,t)] + shortage[(s,p,t)] == demand[t][s][p], f"DemandSat_{s}_{p}_{t}"

# 5) Flow conservation: what stations consume must equal sum of shipments to that station that period (across bases and modes)
for t in Periods:
    for s in Stations:
        for p in Parts:
            model += pulp.lpSum([ship_truck[(b,s,p,t)] + ship_air[(b,s,p,t)] for b in Bases]) == consumed[(s,p,t)], f"Flow_{s}_{p}_{t}"

# 6) Non-negativity already enforced by variable definitions

# ---------------------------
# Solve
# ---------------------------
solver = pulp.PULP_CBC_CMD(msg=1, timeLimit=60)  # show CBC output; set timeLimit to 60s
start = time.time()

# capture solver log
old_stdout = sys.stdout
sys.stdout = mystdout = io.StringIO()
result = model.solve(solver)
sys.stdout = old_stdout
end = time.time()
cbc_log = mystdout.getvalue().splitlines()

# Parse useful info from CBC log
presolve_lines = [l for l in cbc_log if "Presolve" in l]
iter_lines = [l for l in cbc_log if l.strip().split() and l.strip().split()[0].isdigit()]
opt_lines = [l for l in cbc_log if "Optimal" in l and "objective" in l]

# ---------------------------
# Print neat summary
# ---------------------------
print("\n--- Presolve / Model stats ---")
if presolve_lines:
    print(presolve_lines[0])
else:
    # fallback stats (approx)
    print("Presolve info not found in solver log.")

print("\n--- Iterations (parsed) ---")
if iter_lines:
    print("Iteration      Objective")
    for L in iter_lines:
        parts = L.strip().split()
        # some lines are "0  Obj 0 Primal inf  ...", some "3  Obj 1707.5"
        try:
            it = parts[0]
            # locate the token that is parseable as objective float
            obj_token = None
            for token in parts[1:]:
                try:
                    _ = float(token)
                    obj_token = token
                    break
                except:
                    continue
            if obj_token:
                print(f"{int(it):>9} {float(obj_token):>15.6f}")
        except Exception:
            pass
else:
    print("No iteration lines parsed from solver log.")

print("\n--- Final solver line ---")
if opt_lines:
    print(opt_lines[-1])
else:
    print("No explicit 'Optimal' line parsed.")

print(f"Solve Time: {end - start:.6f} seconds\n")

# ---------------------------
# Print decision summaries
# ---------------------------
status = pulp.LpStatus[model.status]
print("Status:", status)
print(f"Objective (Total cost, ₹ thousands): {pulp.value(model.objective):.3f}\n")

# Show orders placed and order qtys
print("Orders placed (Order qty arrives next period):")
order_table = []
for b in Bases:
    for t in Periods:
        for p in Parts:
            q = order_qty[(b,p,t)].value()
            if q is not None and q > 1e-6:
                order_table.append([b, t, p, q])
if order_table:
    print(tabulate(order_table, headers=["Base","Period","Part","OrderQty"], floatfmt=".1f"))
else:
    print("No orders placed.")

# Show shipments per mode aggregated per base-station-part-period
print("\nShipments (Truck / Air) sample rows (nonzero):")
ship_rows = []
for b in Bases:
    for s in Stations:
        for p in Parts:
            for t in Periods:
                st = ship_truck[(b,s,p,t)].value() or 0.0
                sa = ship_air[(b,s,p,t)].value() or 0.0
                if st > 1e-6 or sa > 1e-6:
                    ship_rows.append([b,s,p,t,st,sa])
if ship_rows:
    print(tabulate(ship_rows, headers=["Base","Station","Part","Period","Truck","Air"], floatfmt=".1f"))
else:
    print("No shipments? (unexpected)")

# show inventory snapshot at final period
print("\nInventory at end of each period (sample nonzero entries):")
inv_rows = []
for b in Bases:
    for p in Parts:
        for t in Periods:
            inv = inventory[(b,p,t)].value() or 0.0
            if inv > 1e-6:
                inv_rows.append([b,p,t,inv])
if inv_rows:
    print(tabulate(inv_rows, headers=["Base","Part","Period","Inv_End"], floatfmt=".1f"))
else:
    print("All inventories zero at end of periods.")

# show shortages if any
print("\nShortages (station,part,period):")
sh_rows = []
for s in Stations:
    for p in Parts:
        for t in Periods:
            sh = shortage[(s,p,t)].value() or 0.0
            if sh > 1e-6:
                sh_rows.append([s,p,t,sh])
if sh_rows:
    print(tabulate(sh_rows, headers=["Station","Part","Period","Shortage"], floatfmt=".1f"))
else:
    print("No shortages recorded.")

# End of model
