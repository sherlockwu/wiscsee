import collections
import os
import pprint
import random
import time
import sys
import subprocess

from commons import *
import config
import multiwriters
from utilities import utils

from pyreuse.helpers import *
from pyreuse.apputils.parseleveldboutput import parse_file

class Workload(object):
    def __init__(self, confobj, workload_conf_key = None):
        """
        workload_conf is part of confobj. But we may need to run
        multiple workloads with different configurations in our
        experiements. So we need workload_conf to specify which
        configuration we will use in a Workload instance.

        Since workload_conf has a default value, it should be
        compatible with previous code. However, new classes based
        one Workload should use this new __init__() with two parameters.
        """
        if not isinstance(confobj, config.Config):
            raise TypeError("confobj is not of type class config.Config".
                format(type(confobj).__name__))

        self.conf = confobj
        if workload_conf_key != None and workload_conf_key != 'None':
            self.workload_conf = confobj[workload_conf_key]

    def run(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

class NoOp(Workload):
    """
    This is a workload class that does nothing. It may be used to skip
    the file system aging stage. To skip aging workload, set
    conf['age_workload_class'] = "NoOp"
    """
    def run(self):
        pass

    def stop(self):
        pass


class SimpleRandReadWrite(Workload):
    def __init__(self, confobj, workload_conf_key = None):
        super(SimpleRandReadWrite, self).__init__(confobj, workload_conf_key)

    def run(self):
        mnt = self.conf["fs_mount_point"]
        datafile = os.path.join(mnt, "datafile")
        region = 2 * MB
        chunksize = 64 * KB
        n_chunks = region / chunksize
        chunkids = range(n_chunks)

        buf = "a" * chunksize
        f = open(datafile, "w+")
        random.shuffle(chunkids)
        for chunkid in chunkids:
            offset = chunkid * chunksize
            f.seek(offset)
            f.write(buf)
            os.fsync(f)

        random.shuffle(chunkids)
        for chunkid in chunkids:
            offset = chunkid * chunksize
            f.seek(offset)
            buf = f.read()
            os.fsync(f)

        f.close()

    def stop(self):
        pass


class leveldb_test(Workload):
    def __init__(self, confobj, workload_conf_key = None):
        super(leveldb_test, self).__init__(confobj, workload_conf_key)

    def run(self):
        mnt = self.conf["fs_mount_point"]
        os.chdir(mnt)
        print "====== get in leveldb_test"
        #cmd = "cp -r /users/kanwu/leveldb/app_leveldb/ " + mnt
        #subprocess.call(cmd, shell=True)
	app_leveldb = "/users/kanwu/leveldb/app_leveldb/"
        os.chdir(app_leveldb)
        cmd = "./run_experiment.sh fillread"
        subprocess.call(cmd, shell=True)

    def stop(self):
        pass

class external_sort_bench(Workload):
    def __init__(self, confobj, workload_conf_key = None):
        super(external_sort_bench, self).__init__(confobj, workload_conf_key)

    def run(self):
        mnt = self.conf["fs_mount_point"]
        os.chdir(mnt)
        print "====== get in external sorting benchmark"
        #cmd = "cp -r /users/kanwu/leveldb/app_leveldb/ " + mnt
        #subprocess.call(cmd, shell=True)
	app_external_sort = "/users/kanwu/External_Sorting/code/"
        os.chdir(app_external_sort)
        #cmd = "./merge_sort 16777216 4"
        cmd = "./merge_sort 65536 4"
        print "====== executing ", cmd
        subprocess.call(cmd, shell=True)

    def stop(self):
        pass

# class LinuxDD(Workload):
    # def __init__(self, confobj, workload_conf_key = None):
        # super(LinuxDD, self).__init__(confobj, workload_conf_key)

    # def run(self):
        # mnt = self.conf["fs_mount_point"]
        # cmd = "dd if=/dev/zero of={}/datafile bs=64k count=128".format(mnt)
        # print cmd
        # subprocess.call(cmd, shell=True)
        # subprocess.call("sync")

    # def stop(self):
        # pass


