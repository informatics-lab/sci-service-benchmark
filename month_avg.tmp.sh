#!/bin/bash -l
#SBATCH --qos=normal
#SBATCH --mem=8000
#SBATCH --ntasks=4
#SBATCH --output=/home/h04/tmccaie/sci-service-benchmark-D-12-out.log
#SBATCH --error=/home/h04/tmccaie/sci-service-benchmark-D-12-error.log
#SBATCH --time=360
#SBATCH --mail-user=theo.mccaie@metoffice.gov.uk
#SBATCH --mail-type=ALL

python2.7 spice_monthly_climate.py  12 D '/project/spice/informatics_lab/mogreps-g/2016/'
