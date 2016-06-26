import socket
import unittest
import time

import workrunner
import ssdbox
from utilities import utils
from config import MountOption as MOpt
from workflow import run_workflow
from ssdbox.ssdframework import classify_lpn_in_gclog, get_range_table

class TestCpuhandler(unittest.TestCase):
    def test_cpu(self):
        possible_cpus = workrunner.cpuhandler.get_possible_cpus()
        workrunner.cpuhandler.enable_all_cpus()

        online_cpus = workrunner.cpuhandler.get_online_cpuids()
        self.assertListEqual(possible_cpus, online_cpus)

class TestLinuxNCQDepth(unittest.TestCase):
    def test_ncq_depth_setting(self):
        if not 'wisc.cloudlab.us' in socket.gethostname():
            return

        depth = 2
        utils.set_linux_ncq_depth("sdc", depth)
        read_depth = utils.get_linux_ncq_depth("sdc")
        self.assertEqual(depth, read_depth)

class TestSettingScheduler(unittest.TestCase):
    def test_setting(self):
        if not 'wisc.cloudlab.us' in socket.gethostname():
            return

        scheduler = 'noop'
        utils.set_linux_io_scheduler("sdc", scheduler)

        read_scheduler = utils.get_linux_io_scheduler("sdc")
        self.assertEqual(scheduler, read_scheduler)


class Experimenter(object):
    def __init__(self):
        self.conf = ssdbox.dftldes.Config()

    def setup_environment(self):
        self.conf['device_path'] = '/dev/loop0'
        self.conf['dev_size_mb'] = 256
        self.conf['filesystem'] = 'f2fs'
        self.conf["n_online_cpus"] = 'all'

        self.conf['linux_ncq_depth'] = 31

    def setup_workload(self):
        self.conf['workload_class'] = 'NoOp'
        self.conf['NoOp'] = {}
        self.conf['workload_conf_key'] = 'NoOp'

    def setup_fs(self):
        pass
        # self.conf['mnt_opts'].update({
            # "f2fs":   {
                        # 'discard': MOpt(opt_name = 'discard',
                                        # value = 'discard',
                                        # include_name = False),
                        # 'background_gc': MOpt(opt_name = 'background_gc',
                                            # value = 'off',
                                            # include_name = True)
                                        # }
            # }
            # )

    def setup_flash(self):
        pass

    def setup_ftl(self):
        self.conf['enable_blktrace'] = False
        self.conf['enable_simulation'] = False

    def run(self):
        utils.set_exp_metadata(self.conf, save_data = False,
                expname = 'tmp',
                subexpname = 'subtmp')
        utils.runtime_update(self.conf)
        run_workflow(self.conf)

        utils.shcmd("fio -name hello -rw=randwrite -size=16mb -fsync=1  -filename {}/data2"\
                .format(self.conf['fs_mount_point']))
        time.sleep(1)
        ret = utils.invoke_f2fs_gc(self.conf['fs_mount_point'], 1)
        assert ret == 0

    def main(self):
        self.setup_environment()
        self.setup_fs()
        self.setup_workload()
        self.setup_flash()
        self.setup_ftl()
        self.run()


class TestF2FSGCCall(unittest.TestCase):
    def test(self):
        obj = Experimenter()
        obj.main()

class TestImportPyreuse(unittest.TestCase):
    def test(self):
        import prepare4pyreuse
        import pyreuse
        pyreuse.helpers.shcmd("echo 33333")

class TestClassifyGcLOG(unittest.TestCase):
    def test(self):
        classify_lpn_in_gclog("tests/testdata/gc.log",
                "tests/testdata/dumpe2fs.out")


def main():
    unittest.main()

if __name__ == '__main__':
    main()


