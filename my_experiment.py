import collections
import os

from workflow import *
from config_helper import experiment


class my_experiment(experiment.Experiment):
    def setup_workload(self):
       self.conf['workload_class'] = 'leveldb_test'

if __name__=='__main__':
    # set parameters
    para = experiment.get_shared_nolist_para_dict("leveldb_test", 16*MB)   # get shared parameters
    para['device_path'] = "/dev/sdc1"
    para['filesystem'] = "ext4"
    para['ftl'] = "dftldes"
    para['lbabytes'] = 1024*1024*1024 
    Parameters = collections.namedtuple("Parameters", ','.join(para.keys()))

    # run this experiment
    obj = my_experiment( Parameters(**para) )
    obj.main()
    
