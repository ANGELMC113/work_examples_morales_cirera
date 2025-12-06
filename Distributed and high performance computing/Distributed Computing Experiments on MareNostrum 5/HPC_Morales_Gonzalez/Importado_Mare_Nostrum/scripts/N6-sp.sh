#!/bin/bash
#SBATCH --job-name=sp-mz 
#SBATCH --output=../logs/sp-mz/sp-mz_%j.out 
#SBATCH --error=../logs/sp-mz/sp-mz_%j.err 
#SBATCH --ntasks=672 
#SBATCH --cpus-per-task=1 
#SBATCH --qos=gp_debug 
#SBATCH --account=nct_321 

export NAS_PATH=$HOME/proyectoHPC/NPB3.4.3-MZ/NPB3.4-MZ-MPI/bin 

srun --ear=on --ear-user-db=sp-N6_metrics --ntasks=672 --cpus-per-task=1 $NAS_PATH/sp-mz.D.x
srun --ear=on --ear-user-db=sp-N6_metrics --ntasks=336 --cpus-per-task=2 $NAS_PATH/sp-mz.D.x 
srun --ear=on --ear-user-db=sp-N6_metrics --ntasks=84 --cpus-per-task=8 $NAS_PATH/sp-mz.D.x
srun --ear=on --ear-user-db=sp-N6_metrics --ntasks=48 --cpus-per-task=14 $NAS_PATH/sp-mz.D.x
srun --ear=on --ear-user-db=sp-N6_metrics --ntasks=12 --cpus-per-task=56 $NAS_PATH/sp-mz.D.x 
srun --ear=on --ear-user-db=sp-N6_metrics --ntasks=6 --cpus-per-task=112 $NAS_PATH/sp-mz.D.x 
