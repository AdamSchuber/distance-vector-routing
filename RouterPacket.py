#!/usr/bin/env python

from copy import deepcopy

class RouterPacket(object):
    sourceid = None         #  id of sending router sending this pkt
    destid   = None         #  id of router to which pkt being sent
                            #  (must be an immediate neighbor)
    mincost  = None         #  min cost to node 0 ... 3

    def __init__(self, sourceID, destID, mincosts):
        super(RouterPacket, self).__init__()
        self.sourceid = sourceID
        self.destid = destID
        self.mincost = deepcopy(mincosts)

    def clone(self):
        return RouterPacket(self.sourceid, self.destid, deepcopy(self.mincost))
