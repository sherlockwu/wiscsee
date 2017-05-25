import json
import sys
import os

# get home dir
result_dir = sys.argv[1]
print '=== handling ' + result_dir
os.chdir(result_dir)

result = []
# for each sub-dir
for sub_exp in os.listdir('./'):
    # read recorder.json
    with open('./'+sub_exp+'/recorder.json') as data_file: 
	data = json.load(data_file)
        
        # get miss ratio
    	hit_count = int(data['general_accumulator']['Mapping_Cache']['hit'])
    	miss_count = int(data['general_accumulator']['Mapping_Cache']['miss'])
        overall = hit_count + miss_count
        miss_ratio = (float(miss_count) / float(overall))
        print 'hit: ' + str(hit_count) + ' miss: ' + str(miss_count)
        print 'miss ratio: ' + str(miss_ratio)
        result.append(miss_ratio)

print sorted(result, reverse=True)
