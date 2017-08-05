from commons import *
from ftlsim_commons import *
import hostevent
# Kan: dependency_aware
import dependency

class Host(object):
    def __init__(self, conf, simpy_env, event_iter):
        self.conf = conf
        self.env = simpy_env
        self.event_iter = event_iter
 
        print '======== ncq_depth of SSD: ', self.conf['SSDFramework']['ncq_depth']
        self._ncq = NCQSingleQueue(
                ncq_depth = self.conf['SSDFramework']['ncq_depth'],
                simpy_env = self.env)

        # init the dependency graph
        print "\n\n\n=============\n", self.conf['dependency_knowledge_path'], "\n============\n\n\n"
        dependency.init(self.conf['dependency_knowledge_path'])

    def get_ncq(self):
        return self._ncq

    def _process(self):
        # Kan: dependency-aware to distribute events to ncq TODO
        for event in self.event_iter:
            if isinstance(event, hostevent.Event) and event.offset < 0:
                # due to padding, accesing disk head will be negative.
                continue

            if event.action == 'D':
                print '!!!', event
        
        for event in self.event_iter:
            if isinstance(event, hostevent.Event) and event.offset < 0:
                # due to padding, accesing disk head will be negative.
                continue

            if event.action == 'D':
                print '=== handling: ', event
                yield self._ncq.queue.put(event)

    def run(self):
        yield self.env.process(self._process())
        yield self._ncq.queue.put(hostevent.ControlEvent(OP_SHUT_SSD))


