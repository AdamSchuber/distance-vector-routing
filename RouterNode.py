#!/usr/bin/env python
import GuiTextArea
import RouterPacket
import F
from copy import deepcopy


class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None            #Cost for the link between two nodes
    distVector = None       #The shortest distance to every node
    graph = None

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.export DISPLAY=172.25.32.1:0.0

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea(
            "  Output window for Router #" + str(ID) + "  ") 
        self.costs = deepcopy(costs)
        self.distVector = deepcopy(costs)
        
        # Send distVector to adjacent nodes
        for nodeID in range(0, len(self.costs)):
            if self.is_adjacent(nodeID):
                pkt = RouterPacket.RouterPacket(self.myID, nodeID, self.distVector)
                self.sendUpdate(pkt)
    # --------------------------------------------------
    def is_adjacent(self, nodeID):
        return nodeID != self.myID and self.costs[nodeID] != 999

    # --------------------------------------------------
    def updateDistVector(self, costs, sourceID):
        pass
        # Dx(Y) min{c(x,y) + Dy(y), c(x,z) + Dz(y)}

        # D1(0) min{cost(1,0) + D0(0), cost(1,2) + D2(1)}
        # D1(0) min{4 + 0, 50 + 1}
        # D1(0) = cost(1,0) = 4

        # thirdWheel = 0
        # if thirdWheel == self.myID or thirdWheel == pkt.sourceID:
        #     thirdWheel += 1
        # if thirdWheel == self.myID or thirdWheel == pkt.sourceID:
        #     thirdWheel += 1

        # self.distVector[sourceID] = min(
        #     costs[self.myID] + self.distVector[self.myID], costs[thirdWheel] + self.distVector[thridWheel])

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        if not self.myID == pkt.sourceid:
            pass
            # Node 1: 4 0 50 - src
            # Node 0: 0 4 1  - dest
            # self.costs[pkt.sourceid] = pkt.mincosts[self.myID]
            # # Node 0: 0 60 1 - dest
            # self.updateDistVector(self, pkt.mincosts, pkt.sourceid)

    # --------------------------------------------------
    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)

    # --------------------------------------------------

    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        self.myGUI.println("")
        self.myGUI.println("Distancetable:")
        self.myGUI.println("      dst |    0   1   2")
        self.myGUI.println("--------------------------")
        self.myGUI.print(" nbr    " + str(self.myID) + " |    " + str(self.costs[0]) + "   " +
                         str(self.costs[1]) + "   " + str(self.costs[2]) + "\n")

    # --------------------------------------------------

    def updateLinkCost(self, dest, newcost):
        pass
        # self.costs[dest] = newcost
        # self.updateDistVector(self, self.costs, dest)
        # self.sendUpdate()
