#!/bin/bash
#SBATCH --job-name=tensorflow 
#SBATCH --output=logs/%J.out 
#SBATCH --error=logs/%J.err 
#SBATCH -N 1 
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=20 
#SBATCH --qos=acc_debug 
#SBATCH --account=nct_321 
#SBATCH -t 00:30:00 
#SBATCH --gres=gpu:1 
#SBATCH --ear=on 
#SBATCH --ear-user-db=metrics_tensorflow 
#SBATCH --constraint=perfparanoid 
 
module load tensorflow/2.16.1  
export OMP_NUM_THREADS=18 
export EARL_REPORT_LOOPS=1 
 
 
 
# model, mixed-prec and disable-tf32 
srun -J ResNet50 python benchmark.py  --model=ResNet50 --num-iters=100 
srun -J ResNet50_mixed python benchmark.py --mixed-prec --num-iters=100 
srun -J ResNet50_disable-tf32 python benchmark.py --model=ResNet50 --disable-tf32 --num-iters=100 
srun -J VGG19 python benchmark.py  --model=VGG19 --num-iters=100 
srun -J VGG19_mixed python benchmark.py  --model=VGG19 --mixed-prec --num-iters=100 
srun -J VGG19_disable-tf32 python benchmark.py  --model=VGG19 --disable-tf32 --num-iters=100 
srun -J DenseNet121 python benchmark.py  --model=DenseNet121 --numiters=100 
srun -J DenseNet121_mixed python benchmark.py  --model=DenseNet121 --mixed-prec --num-iters=100
srun -J DenseNet121_disable-tf32 python benchmark.py  --model=DenseNet121 --disable-tf32 --num-iters=100