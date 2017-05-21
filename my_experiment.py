import collections
import os

from workflow import *
from config_helper import experiment
import config

class my_experiment(experiment.Experiment):
    def setup_workload(self):
       self.conf['workload_class'] = 'leveldb_test'

if __name__=='__main__':
    # set parameters
    para = experiment.get_shared_nolist_para_dict("leveldb_test", 256*MB)   # get shared parameters
    para['device_path'] = "/dev/sdc1"
    para['filesystem'] = "f2fs"
    #para['ftl'] = "nkftl2"
    para['ftl'] = "dftldes"
    para['do_gc_after_workload'] = True
    # for data block group
    #para['segment_bytes'] = 0.5*MB
    #para['log_group_factor'] = 1
    #para['over_provisioning'] = 32

    Parameters = collections.namedtuple("Parameters", ','.join(para.keys()))

    # run this experiment
    obj = my_experiment( Parameters(**para) )
    obj.main()
