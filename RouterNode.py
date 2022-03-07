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

        # Initilizes distanceVector as Matrix with the nodes as columns and rows
        self.distanceVector = [
            [0 for _ in range(self.sim.NUM_NODES)] for _ in range(self.sim.NUM_NODES)]

        # Initilizes distanceVector to infinity to all nodes except itself
        for i in range(self.sim.NUM_NODES):
            for j in range(self.sim.NUM_NODES):
                if not i == ID and j == ID:
                    self.distanceVector[i][j] = self.sim.INFINITY
                else:
                    self.distanceVector[i][j] = 0

        # Initilizes the self nodes costs to neighbors
        self.distanceVector[self.myID] = self.costs

        # Sends update packet if nodes are adjecent

        # for nodeID in range(0, self.sim.NUM_NODES):
        #     if self.isAdjacent(nodeID):
        #         pkt = RouterPacket.RouterPacket(
        #             self.myID, nodeID, self.distanceVector)
        #         self.sendUpdate(pkt)

        # Tänker att vi borde skicka array istället för matrix
        for nodeID in range(0, self.sim.NUM_NODES):
            if self.isAdjacent(nodeID):
                pkt = RouterPacket.RouterPacket(
                    self.myID, nodeID, self.distanceVector[self.myID])
                self.sendUpdate(pkt)

    # --------------------------------------------------
    def isAdjacent(self, nodeID):
        return nodeID != self.myID and self.costs[nodeID] != 999

    # --------------------------------------------------

    def updateDistanceVector(self, mincost, sourceID):
        # Dx(y) min{c(x,y) + Dy(y), c(x,z) + Dz(y)}
        for nodeID in range(self.sim.NUM_NODES):
            # self.distanceVector[self.myID][nodeID] = min(
            #     mincost[self.myID][nodeID] + mincost[self.myID][self.myID], mincost[sourceID][nodeID] + mincost[sourceID][self.myID])
            self.distanceVector[self.myID][nodeID] = min(
                self.costs[nodeID] + self.costs[self.myID], mincost[nodeID] + mincost[self.myID])

    # --------------------------------------------------

    def recvUpdate(self, pkt):
        if not self.myID == pkt.sourceid:
            self.costs[pkt.sourceid] = pkt.mincost[self.myID]
            self.updateDistanceVector(pkt.mincost, pkt.sourceid)

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
        # self.myGUI.print(" nbr    " + str(self.myID) + " |    " + str(self.costs[0]) + "   " +
        #                  str(self.costs[1]) + "   " + str(self.costs[2]) + "\n")
        for nodeID in range(0, self.sim.NUM_NODES):
            self.myGUI.print(" nbr    " + str(nodeID) + " |    ")
            for i in range(0, self.sim.NUM_NODES):
                self.myGUI.print(str(self.distanceVector[nodeID][i]) + "   ")
            self.myGUI.print("\n")

    # --------------------------------------------------

    def updateLinkCost(self, destID, newcost):
        # Update costs for self
        # self.costs[destID] = newcost
        # self.updateDistanceVector()

        # Send update to all adjencent nodes
        pass
