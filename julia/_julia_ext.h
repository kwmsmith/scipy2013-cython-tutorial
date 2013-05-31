/*-----------------------------------------------------------------------------
 * Copyright (c) 2012, Enthought, Inc.
 * All rights reserved.  See LICENSE.txt for details.
 *  
 * Author: Kurt W. Smith
 * Date: 26 March 2012
 --------------------------------------------------------------------------*/

#ifndef __JULIA_EXT_H__
#define __JULIA_EXT_H__

#include <complex.h>

typedef double complex cpx_t;
typedef double         real_t;

unsigned int julia_kernel(cpx_t, cpx_t, real_t, real_t);

unsigned int *compute_julia(cpx_t, unsigned int, real_t, real_t);

#endif
