/*-----------------------------------------------------------------------------
 * Copyright (c) 2012, Enthought, Inc.
 * All rights reserved.  See LICENSE.txt for details.
 *  
 * Author: Kurt W. Smith
 * Date: 26 March 2012
 --------------------------------------------------------------------------*/

#include "_julia_ext.h"
#include <stdlib.h>

#define CABS_SQ(z) (creal(z) * creal(z) + cimag(z) * cimag(z))

unsigned int
julia_kernel(cpx_t z,
             cpx_t c,
             real_t lim,
             real_t cutoff)
{
    unsigned int count = 0;
    real_t lim_sq = lim * lim;

    while(CABS_SQ(z) < lim_sq && count < cutoff) {
        z = z * z + c;
        count++;
    }
    return count;
}

unsigned int *
compute_julia(cpx_t c,
              unsigned int N,
              real_t bound,
              real_t lim)
{
    int i, j, idx;
    real_t step, x, y;

    unsigned int *julia = NULL;
    real_t *grid = NULL;

    julia = (unsigned int*)malloc(N * N * sizeof(unsigned int));
    if(!julia)
        return NULL;

    grid = (real_t*)malloc(N * sizeof(real_t));
    if(!grid)
        goto fail_grid;

    step = (2.0 * bound) / (N-1);
    for(i=0; i < N; i++)
        grid[i] = -bound + i * step;

#pragma omp parallel for \
    shared(grid, julia, c, lim) private(i,j,idx,x,y)
    for(i=0; i < N; i++) {
        x = grid[i];
        for(j=0; j < N; j++) {
            y = grid[j];
            idx = j + N * i;
            julia[idx] = julia_kernel(x + y * I, c, lim, 1e6);
        }
    }

    goto success;

fail_grid:
    if(julia)
        free(julia);
    julia = NULL;
success:
    if(grid)
        free(grid);
    grid = NULL;
    return julia;
}
