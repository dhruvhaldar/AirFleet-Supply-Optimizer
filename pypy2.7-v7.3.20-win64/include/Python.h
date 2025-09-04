
/* Partial C-API headers to allow CFFI C-compiled modules to work with PyPy */
#include <sys/types.h>
#include <stdarg.h>

#ifdef __GNUC__
#define _GNU_SOURCE 1
#endif
#ifndef _WIN32
# define Py_DEPRECATED(VERSION_UNUSED) __attribute__((__deprecated__))
# define PyAPI_FUNC(RTYPE) __attribute__((visibility("default"))) RTYPE
# define PyAPI_DATA(RTYPE) extern PyAPI_FUNC(RTYPE)
# define Py_LOCAL_INLINE(type) static inline type
#else
# define Py_DEPRECATED(VERSION_UNUSED)
#  define PyAPI_FUNC(RTYPE) __declspec(dllimport) RTYPE
#  define PyAPI_DATA(RTYPE) extern __declspec(dllimport) RTYPE
# define Py_LOCAL_INLINE(type) static __inline type __fastcall
#endif

typedef void PyObject;
/* CPython sets Py_ssize_t in pyport.h, PyPy in cpyext_object.h */
#ifdef _WIN64
typedef long long Py_ssize_t;
#else
typedef long Py_ssize_t;
#endif

#include <patchlevel.h>
#include <modsupport.h>

#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <locale.h>
#include <ctype.h>

/* normally defined in "pythread.h", but we can't include that */
#define WITH_THREAD
