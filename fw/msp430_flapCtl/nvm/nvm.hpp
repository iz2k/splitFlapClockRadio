
#ifndef VAR_DEFS          // Make sure this file is included only once
#define VAR_DEFS 1

#include <stdint.h>
/*----------------------------------------------
Setup variable declaration macros.
----------------------------------------------*/
#ifndef VAR_DECLS
# define _DECL extern
# define _INIT(x)
#else
# define _DECL
# define _INIT(x)  = x
#endif

/*----------------------------------------------
Declare variables as follows:

_DECL [standard variable declaration] _INIT(x);

where x is the value with which to initialize
the variable.  If there is no initial value for
the variable, it may be declared as follows:

_DECL [standard variable declaration];
----------------------------------------------*/

// SMBUS NON-VOLATILE REGISTERS
#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  fw_version   _INIT(0x0100);

/* HH */
#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  hh_ir_threshold   _INIT(1);

#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  hh_hall_threshold   _INIT(2);

#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint8_t  hh_hall_digit   _INIT(3);

/* MM */
#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  mm_ir_threshold   _INIT(4);

#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  mm_hall_threshold   _INIT(5);

#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint8_t  mm_hall_digit   _INIT(6);

/* WW */
#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  ww_ir_threshold   _INIT(7);

#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint16_t  ww_hall_threshold   _INIT(8);

#ifdef VAR_DECLS
#pragma PERSISTENT
#endif
_DECL uint8_t  ww_hall_digit   _INIT(9);



#endif

