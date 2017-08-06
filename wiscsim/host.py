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
        dependency.init(self.conf['dependency_knowledge_path'], simpy_env)

    def get_ncq(self):
        return self._ncq

    def _process(self):
        # Kan: dependency-aware to distribute events to ncq
        # initialize bio status(not issued to ncq), and register it to correpsonding node
        to_issue = []
        for event in self.event_iter: 
            if isinstance(event, hostevent.Event) and event.offset < 0:
                # due to padding, accesing disk head will be negative.
                continue

            if event.action == 'D':
                to_issue.append(event)
                node_key = event.get_node()
                if node_key != None:
                    node_key = tuple(node_key.strip('()').replace('\'','').split(','))
                    dependency.register(node_key)    # register
        
        while len(to_issue)>0:
            # handle control event
            has_not_issued_rw = False
            bio_index = 0
            issued = []
            for event in to_issue:
                if isinstance(event, hostevent.ControlEvent):
                    if has_not_issued_rw:    #control event is like a barrier, wait all previous bio finish
                        break
                node_key = event.get_node()
                if node_key != None:
                    node_key = tuple(node_key.strip('()').replace('\'','').split(','))
                    if dependency.judge_status(node_key):
                        issued.insert(0, bio_index)
                        #print 'to issue'
                        yield self._ncq.queue.put(event)
                    else:
                        has_not_issued_rw = True
                else:
                    issued.insert(0, bio_index)
                    #if not isinstance(event, hostevent.ControlEvent):
                    #    print 'to issue'
                    yield self._ncq.queue.put(event)
                bio_index += 1
            # delete issued bios
            for num in issued:
                del to_issue[num]
            # wait until a node's status is changed
            yield self.env.process(dependency.wait_change())
            #yield self.env.timeout(10000)

    def run(self):
        yield self.env.process(self._process())
        yield self._ncq.queue.put(hostevent.ControlEvent(OP_SHUT_SSD))


