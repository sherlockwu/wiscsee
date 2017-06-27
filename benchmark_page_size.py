import collections
import os

from workflow import *
from config_helper import experiment


class my_experiment(experiment.Experiment):
    def setup_workload(self):
        self.conf["workload_src"] = LBAGENERATOR
        self.conf["lba_workload_class"] = "BlktraceEvents"
        self.conf['lba_workload_configs']['mkfs_event_path'] = \
                self.para.mkfs_path
        self.conf['lba_workload_configs']['ftlsim_event_path'] = \
                self.para.ftlsim_path

def run_exps_counter(para):
    #para = experiment.get_shared_nolist_para_dict("test_exp_TestUsingExistingTraceToStudyRequestScale_jj23hx", 1*GB)
    para.update({
        'ftl': "ftlcounter",
        #"mkfs_path": "./tests/testdata/sqlitewal-update/subexp-7928737328932659543-ext4-10-07-23-50-10--2726320246496492803/blkparse-events-for-ftlsim-mkfs.txt",
        #"ftlsim_path": "./tests/testdata/sqlitewal-update/subexp-7928737328932659543-ext4-10-07-23-50-10--2726320246496492803/blkparse-events-for-ftlsim.txt",
        'ftl' : 'ftlcounter',
        'enable_simulation': True,
        'dump_ext4_after_workload': True,
        'only_get_traffic': False,
        'trace_issue_and_complete': True,
        'do_dump_lpn_sem': False,
        })
    submit_exp(para)


def submit_exp(para):
    Parameters = collections.namedtuple("Parameters", ','.join(para.keys()))

    # run this experiment
    obj = my_experiment( Parameters(**para) )
    obj.main()

def run_exps(page_size_set, n_pages_per_block_set, n_channels_set, cache_coverage_set, n_stripe_size_set, n_segment_bytes_set):
    # print
    for page_size in page_size_set:
        print 'page_size: ', page_size
        for n_pages_per_block in n_pages_per_block_set:
            print 'pages_per_block: ', n_pages_per_block
            for n_channels in n_channels_set:
                print 'channels: ', n_channels
                for n_stripe_size in n_stripe_size_set:
                    print 'stripe_size: ', n_stripe_size, ' block'
                    for n_segment_bytes in n_segment_bytes_set:
                    	print 'segment_bytes: ', n_segment_bytes, ' MB'
                    	
			# set the output exp name
                    	exp_name = 'sort_2_14_segment_' + str(n_segment_bytes) + '_pagesize_' + str(page_size) + '_pagesperblock_' + str(n_pages_per_block) + '_channels_' + str(n_channels) + '_stripepage_' + str(n_stripe_size)
                    	print '============================ genearting ' , exp_name
                    	
                    	for cache_coverage in cache_coverage_set:
                        	print 'cache_coverage: ', cache_coverage
                        	para = experiment.get_shared_nolist_para_dict(exp_name, 256*MB)
                        	para.update({
                            	'ftl': "dftldes",
                            	"mkfs_path": "/tmp/results/trace_external_merge_sort/2_20_ratio_16/blkparse-events-for-ftlsim-mkfs.txt",
                            	"ftlsim_path": "/tmp/results/trace_external_merge_sort/2_20_ratio_16/blkparse-events-for-ftlsim.txt",
                            	'ssd_ncq_depth': 8, # For Queue Depth test
                                'segment_bytes': n_segment_bytes*1024*1024,
                            	'page_size': page_size*1024,
                            	'n_pages_per_block': n_pages_per_block,
                            	'n_channels_per_dev': n_channels,
                            	'stripe_size': int(n_stripe_size),
                            	'cache_mapped_data_bytes': int(8589934592*cache_coverage),
                        	})
                        # For counter:
                        #run_exps_counter(para)
                        submit_exp(para)


    # set some parameters

    # submit_exp

    #for n_channels in n_channels_set:
    #    para['n_channels_per_dev'] = n_channels      # channels
    #    for n_pages_per_block in n_pages_per_block_set:
    #        para['n_pages_per_block'] =  n_pages_per_block     # pages per block
    #        para['stripe_size'] = n_pages_per_block/4
            # submit experiment
   	    
    #        'n_pages_per_block': 128,
    #        'cache_mapped_data_bytes': 268435456*0.5,
            
    #         submit_exp(para)

if __name__=='__main__':
    # set parameters
    
    # run experiments with different parameters
    # page_size_set = [2, 4, 8]   16 maybe?
    page_size_set = [2]
    
    # n_pages_per_block_set = [64, 128, 256]
    n_pages_per_block_set = [256]
    
    #n_channels_set = [4, 8, 16]
    n_channels_set = [16]

    # cache_coverage_set = [0.01, 0.05, 0.1, 0.5, 1]
    cache_coverage_set = [1]
    
    # n_stripe_size_set = [0.25, 0.5, 1] of block or units of pages
    n_stripe_size_set = [1]

    # segment_bytes = [2, 16, 64, 128]
    n_segment_bytes_set = [1024]

    run_exps(page_size_set, n_pages_per_block_set, n_channels_set, cache_coverage_set, n_stripe_size_set, n_segment_bytes_set)
