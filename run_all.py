import os
import subprocess

script = """#!/bin/bash -l
#SBATCH --qos=normal
#SBATCH --mem=8000
#SBATCH --ntasks=4
#SBATCH --output=/home/h04/tmccaie/sci-service-benchmark-{region}-{month}-out.log
#SBATCH --error=/home/h04/tmccaie/sci-service-benchmark-{region}-{month}-error.log
#SBATCH --time=360
#SBATCH --mail-user=theo.mccaie@metoffice.gov.uk
#SBATCH --mail-type=ALL

python2.7 spice_monthly_climate.py  {month} {region} '/project/spice/informatics_lab/mogreps-g/2016/'
"""

scriptname = 'month_avg.tmp.sh'
for region in ['A', 'B', 'C', 'D']:
    for month in range(1,13):
        with open(scriptname, 'w') as fp:
            fp.write(script.format(region=region, month=str(month)))
        os.chmod(scriptname, 0o744)
        subprocess.call(['sbatch', scriptname])
        
