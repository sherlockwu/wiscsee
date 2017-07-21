import collections
import os

from workflow import *
from config_helper import experiment
import config

class my_experiment(experiment.Experiment):
    def setup_workload(self):
       self.conf['workload_class'] = 'external_sort_bench'

if __name__=='__main__':
    # set parameters
    para = experiment.get_shared_nolist_para_dict("trace_external_merge_sort", 128*GB)   # get shared parameters
    para.update({
                            	'ftl': "ftlcounter",
                            	'ssd_ncq_depth': 32, # For Queue Depth test
                                'segment_bytes': 128*1024*1024,
                                'trace_issue_and_complete': True, # For trace ncq C
                            	'page_size': 2*1024,
                            	'n_pages_per_block': 256,
                            	'n_channels_per_dev': 16,
                            	'stripe_size': 256,
                            	'cache_mapped_data_bytes': 268435456,
                                'only_get_traffic': False,
    })
    para['device_path'] = "/dev/sdc1"
    para['filesystem'] = "ext4"
    #para['ftl'] = "ftlcounter" # for see ncq_depth
    para['enable_simulation'] = True
    para['do_ncq_depth_time_line'] = True
    #para['do_gc_after_workload'] = True

    Parameters = collections.namedtuple("Parameters", ','.join(para.keys()))

    # run this experiment
    obj = my_experiment( Parameters(**para) )
    obj.main()
