import collections
import os

from workflow import *
from config_helper import experiment
import config

class my_experiment(experiment.Experiment):
    def setup_workload(self):
        self.conf["workload_src"] = LBAGENERATOR
        self.conf["lba_workload_class"] = "BlktraceEvents"
        self.conf['lba_workload_configs']['mkfs_event_path'] = \
                self.para.mkfs_path
        self.conf['lba_workload_configs']['ftlsim_event_path'] = \
                self.para.ftlsim_path

if __name__=='__main__':
    para = experiment.get_shared_nolist_para_dict("simulate_test", 256*MB)
    para.update({
            'ftl': "dftldes",
            "mkfs_path": "/users/kanwu/wiscsee/benchmark_files/fillrandom/blkparse-events-for-ftlsim-mkfs.txt",
            "ftlsim_path": "/users/kanwu/wiscsee/benchmark_files/fillrandom/blkparse-events-for-ftlsim.txt",
   	    'n_pages_per_block': 128,
            'cache_mapped_data_bytes': 268435456*0.5,
    })

    Parameters = collections.namedtuple("Parameters", ','.join(para.keys()))
    obj = my_experiment( Parameters(**para) )
    obj.main()
