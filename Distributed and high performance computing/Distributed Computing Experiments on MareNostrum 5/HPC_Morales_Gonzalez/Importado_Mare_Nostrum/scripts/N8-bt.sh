#!/bin/bash
#SBATCH --job-name=bt-mz 
#SBATCH --output=../logs/bt-mz/bt-mz_%j.out 
#SBATCH --error=../logs/bt-mz/bt-mz_%j.err 
#SBATCH --ntasks=896 
#SBATCH --cpus-per-task=1 
#SBATCH --qos=gp_debug 
#SBATCH --account=nct_321 

export NAS_PATH=$HOME/proyectoHPC/NPB3.4.3-MZ/NPB3.4-MZ-MPI/bin 

srun --ear=on --ear-user-db=bt-N8_metrics --ntasks=896 --cpus-per-task=1 $NAS_PATH/bt-mz.D.x
srun --ear=on --ear-user-db=bt-N8_metrics --ntasks=448 --cpus-per-task=2 $NAS_PATH/bt-mz.D.x 
srun --ear=on --ear-user-db=bt-N8_metrics --ntasks=112 --cpus-per-task=8 $NAS_PATH/bt-mz.D.x
srun --ear=on --ear-user-db=bt-N8_metrics --ntasks=64 --cpus-per-task=14 $NAS_PATH/bt-mz.D.x
srun --ear=on --ear-user-db=bt-N8_metrics --ntasks=16 --cpus-per-task=56 $NAS_PATH/bt-mz.D.x 
srun --ear=on --ear-user-db=bt-N8_metrics --ntasks=8 --cpus-per-task=112 $NAS_PATH/bt-mz.D.x 
