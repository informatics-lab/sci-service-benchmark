#!/bin/bash -l                       
#SBATCH --qos=normal                 
#SBATCH --mem=8000                   
#SBATCH --ntasks=1                  
#SBATCH --output=/home/h04/tmccaie/sci-service-benchmark-out.log   
#SBATCH --error=/home/h04/tmccaie/sci-service-benchmark-error.log 
#SBATCH --time=120               
#SBATCH --mail-user=theo.mccaie@metoffice.gov.uk
#SBATCH --mail-type=ALL

python2.7 spice_monthly_climate.py  7 B '/project/spice/informatics_lab/mogreps-g-sub/'
