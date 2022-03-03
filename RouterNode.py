#!/usr/bin/env python
import GuiTextArea
import RouterPacket
import F
from copy import deepcopy


class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None
    distanceVector = None

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.export DISPLAY=172.25.32.1:0.0

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea(
            "  Output window for Router #" + str(ID) + "  ")
        self.costs = deepcopy(costs)

        self.distanceVector = [
            [0 for _ in range(self.sim.NUM_NODES)] for _ in range(self.sim.NUM_NODES)]

        for i in range(self.sim.NUM_NODES):
            for j in range(self.sim.NUM_NODES):
                if not i == ID and j == ID:
                    self.distanceVector[i][j] = self.sim.INFINITY
                else:
                    self.distanceVector[i][j] = 0

        self.updateDistanceVector(costs, ID)

        for nodeID in range(0, self.sim.NUM_NODES):
            if self.is_adjacent(nodeID):
                pkt = RouterPacket.RouterPacket(
                    self.myID, nodeID, self.distanceVector)
                self.sendUpdate(pkt)

    # --------------------------------------------------
    def is_adjacent(self, nodeID):
        return nodeID != self.myID and self.costs[nodeID] != 999

    # --------------------------------------------------

    def updateDistanceVector(self, mincosts, sourceid):
        # Dx(y) min{c(x,y) + Dy(y), c(x,z) + Dz(y)}f
        for nodeID in range(self.sim.NUM_NODES):
            self.distanceVector[self.myID][nodeID] = min(
                self.costs[nodeID] + self.costs[self.myID], mincosts[nodeID] + mincosts[self.myID])

    # --------------------------------------------------

    def recvUpdate(self, pkt):
        if not self.myID == pkt.sourceid:
            self.costs[pkt.sourceid] = pkt.mincosts[self.myID]
            self.updateDistanceVector(self, pkt.mincosts, pkt.sourceid)

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
        self.costs[dest] = newcost
        self.updateDistanceVector(self, self.costs, dest)
        self.sendUpdate()
