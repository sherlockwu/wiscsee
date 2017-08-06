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
        # Kan: dependency-aware to distribute events to ncq TODO
        to_issue = []
        print to_issue
        # initialize bio status(not issued to ncq), and register it to correpsonding node
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
            #print "get there =========================\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            # handle control event
            has_not_issued_rw = False
            for event in to_issue:
                if isinstance(event, hostevent.Event) and event.offset < 0:
                    # due to padding, accesing disk head will be negative.
                    continue

                if event.action == 'D':
                    #print 'try :', event
                    if isinstance(event, hostevent.ControlEvent):
                        if has_not_issued_rw:    #control event is like a barrier, wait all previous bio finish
                            #print 'control event barrier'
                            break
                    node_key = event.get_node()
                    if node_key != None:
                        #print '    has node:', node_key
                        node_key = tuple(node_key.strip('()').replace('\'','').split(','))
                        if dependency.judge_status(node_key):
                            to_issue.remove(event)
                            yield self._ncq.queue.put(event)
                        else:
                            has_not_issued_rw = True
                    else:
                        #print '    doesnt have node:'
                        to_issue.remove(event)
                        yield self._ncq.queue.put(event)

            #yield wait until a node's status is changed
            if not dependency.wait_change():
                yield self.env.timeout(100000)

    def run(self):
        yield self.env.process(self._process())
        yield self._ncq.queue.put(hostevent.ControlEvent(OP_SHUT_SSD))


