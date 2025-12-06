#!/bin/bash
#SBATCH --job-name=bt-mz
#SBATCH --output=../logs/bt-mz/bt-mz_%j.out
#SBATCH --error=../logs/bt-mz/bt-mz_%j.err
#SBATCH --ntasks=112
#SBATCH --cpus-per-task=1
#SBATCH --qos=gp_debug
#SBATCH --account=nct_321

export NAS_PATH=$HOME/proyectoHPC/NPB3.4.3-MZ/NPB3.4-MZ-MPI/bin

srun --ear=on --ear-user-db=bt-N1_metrics --ntasks=112 --cpus-per-task=1 $NAS_PATH/bt-mz.D.x
