! CLASS = D
!  
!  
!  This file is generated automatically by the setparams utility.
!  It sets the number of processors and the class of the NPB
!  in this directory. Do not modify it by hand.
!  
        character class
        parameter (class='D')
        integer x_zones, y_zones
        parameter (x_zones=32, y_zones=32)
        integer gx_size, gy_size, gz_size, niter_default
        parameter (gx_size=1632, gy_size=1216, gz_size=34)
        parameter (niter_default=250)
        integer problem_size, kind2
        parameter (problem_size = 98, kind2 = 4)
        double precision dt_default, ratio
        parameter (dt_default = 0.00002d0, ratio = 4.5d0)
        logical  convertdouble
        parameter (convertdouble = .false.)
        character compiletime*11
        parameter (compiletime='03 Mar 2025')
        character npbversion*5
        parameter (npbversion='3.4.3')
        character cs1*6
        parameter (cs1='mpif90')
        character cs2*5
        parameter (cs2='$(FC)')
        character cs3*6
        parameter (cs3='(none)')
        character cs4*6
        parameter (cs4='(none)')
        character cs5*12
        parameter (cs5='-O3 -fopenmp')
        character cs6*9
        parameter (cs6='$(FFLAGS)')
        character cs7*6
        parameter (cs7='randi8')
