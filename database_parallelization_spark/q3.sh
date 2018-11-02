#!/bin/bash
#
# SLURM job submission script Spark example
#
# Job name:
#SBATCH --job-name=q3
#
# Account:
#SBATCH --account=ic_stat243
#
# Partition:
#SBATCH --partition=savio
#
# Resources requested:
#SBATCH --nodes=4
#
# Wall clock limit:
#SBATCH --time=8:00:00
#
module load java spark/2.1.0 python/3.5 
source /global/home/groups/allhands/bin/spark_helper.sh
spark-start
spark-submit --master $SPARK_URL /global/scratch/wejie_yuan/q3.py
spark-stop
