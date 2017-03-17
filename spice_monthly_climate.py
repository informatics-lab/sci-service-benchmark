
# coding: utf-8


# In[12]:

import iris
import os
import datetime
import numpy as np
import sys
import os
import datetime
import time

def timestamp(dt):
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()



# In[3]:

try:
    month = int(sys.argv[1])
    assert month in range(1,13)
except Exception:
    print('Arg 1 must be a month range 1-12.')
    
    
try:
    region_name = sys.argv[2]
    assert region_name in ['A','B','C','D']
except Exception:
    print('Arg 2 must be a refion A, B, C or D.')
    
    
    
try:
    dir_path = sys.argv[3]
    assert os.path.exists(dir_path)
except Exception:
    print('Expect two args, fist a integer month (1-12) second region A, B, C or D.')


print('month', month)


# In[ ]:

lat_con = iris.Constraint(latitude = lambda x : x >= 0)
lon_con = iris.Constraint(longitude = lambda x : x >= 180)
not_lat_con = iris.Constraint(latitude = lambda x : x < 0)
not_lon_con = iris.Constraint(longitude = lambda x : x < 180)

regions = {'A':lat_con & lon_con,
           'B':lat_con & not_lon_con,
           'C':not_lat_con & lon_con,
           'D':not_lat_con & not_lon_con
          }

def file_valid_time(file):
    #     filename_template = 'prods_op_'+MODEL+'_{date}_{run}_{member}_{lead_time}.pp'
    _, _, _, date, run, member, lead_time = os.path.basename(file).split('.')[0].split("_")
    run_date = datetime.datetime(
        int(date[:4]),
        int(date[4:6]),
        int(date[6:8])) 
    valid_time = run_date + datetime.timedelta(hours=int(lead_time)) +  datetime.timedelta(hours=int(run))
    return valid_time

def month_in_file(month, file):
    return file_valid_time(file).month == month
        
def load_stash_for_time_and_region(file, stash, region):
    valid_time_in_hours = timestamp(file_valid_time(file)) / (60 * 60)
    
    return iris.load(file, 
                     iris.AttributeConstraint(STASH=stash) &
                     region &
                     iris.Constraint(time=lambda t: valid_time_in_hours - 0.1 < t < valid_time_in_hours + 0.1 ))


def average_for_month_and_region(month, region, stash, files):
    print('start month:%s, region:%s, stash:%s' % (month, region, stash))
    data_levels = {}
    for cubes in (load_stash_for_time_and_region(f, stash, region) for f in files if month_in_file(month, f)):
        print('Start processing a cube list')
        for cube in cubes:
            print('proces a cube')
            for level_slice in cube.slices(['latitude', 'longitude']):
                level = level_slice.coord('pressure').points[0]
                level_stats = data_levels.get(level, None)
                if not level_stats:
                    aggregated_cube = level_slice
                    count = 1
                else:
                    aggregated_cube = level_stats['cube'] + level_slice
                    count = level_stats['count'] + 1
                data_levels[level] = {
                    'cube':aggregated_cube,
                    'count':count
                }
            print('Done a cube')
    
    print('Create averages')
    results = []
    for level, stats in data_levels.items():
        print('for level %s we have %s slices' % (level, stats['count']))
        results.append(stats['cube'] / stats['count'])
        
    return results


# In[8]:

# Run this thing....
start_time = datetime.datetime.now() 
files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
print("%d files to process in dir %s" % (len(files), dir_path))

avgs = average_for_month_and_region(month,
                                    regions[region_name],
                                    'm01s16i203',
                                    files)

for c in avgs:
    name = "ava_tem_plevel_%d_%s.nc" % (c.coord('pressure').points[0], region_name)
    iris.save(c, os.path.join('/home/h04/tmccaie/sci-service-benchmark-output', name))
    print("Saved %s" % name)


end_time = datetime.datetime.now()
print("Done in %s"  % ( end_time - start_time))
