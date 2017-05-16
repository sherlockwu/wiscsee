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

def run_exps(para, n_channels_set, n_pages_per_block_set):
    # print
    for n_channels in n_channels_set:
        para['n_channels_per_dev'] = n_channels      # channels
        for n_pages_per_block in n_pages_per_block_set:
            print 'channels: '  + str(n_channels) + '\npages per block: ' + str(n_pages_per_block)
            para['n_pages_per_block'] =  n_pages_per_block     # pages per block
            # submit experiment
            submit_exp(para)

if __name__=='__main__':
    # set parameters
    para = experiment.get_shared_nolist_para_dict("leveldb_test", 256*MB)   # get shared parameters
    para['device_path'] = "/dev/sdc1"
    para['filesystem'] = "f2fs"
    para['ftl'] = "dftldes"
    
    # run experiments with different parameters
    #page_size_set = [2, 4, 8, 16]
    #n_pages_per_block_set = [64, 128, 256]
    n_pages_per_block_set = [64]
    n_channels_set = [4, 8, 16]
    run_exps(para, n_channels_set, n_pages_per_block_set)
