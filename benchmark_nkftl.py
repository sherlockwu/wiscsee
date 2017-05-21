import collections
import os

from workflow import *
from config_helper import experiment


class my_experiment(experiment.Experiment):
    def setup_workload(self):
       self.conf['workload_class'] = 'leveldb_test'

def submit_exp(para):
    Parameters = collections.namedtuple("Parameters", ','.join(para.keys()))

    # run this experiment
    obj = my_experiment( Parameters(**para) )
    obj.main()

def run_exps(para, n_segment_bytes_set, n_log_group_factor_set):
    # print
    for n_segment_bytes in n_segment_bytes_set:
        para['segment_bytes'] = n_segment_bytes     # To set block per group
        for n_log_group_factor in n_log_group_factor_set:
            print 'segment bytes: '  + str(n_segment_bytes) + '\nlog group factor: ' + str(n_log_group_factor)
            para['log_group_factor'] =  n_log_group_factor     # factor of log blocks to data blocks
            # submit experiment
            submit_exp(para)

if __name__=='__main__':
    # set parameters
    para = experiment.get_shared_nolist_para_dict("leveldb_test", 256*MB)   # get shared parameters
    para['device_path'] = "/dev/sdc1"
    para['filesystem'] = "f2fs"
    para['ftl'] = "nkftl2"
    
    # run experiments with different parameters
    #segment_bytes = [2, 4, 8, 16]
    #n_pages_per_block_set = [64, 128, 256]
    n_segment_bytes_set = [2*MB, 4*MB, 8*MB]
    n_log_group_factor_set = [10]
    run_exps(para, n_segment_bytes_set, n_log_group_factor_set)
