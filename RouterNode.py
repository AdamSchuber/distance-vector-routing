#!/usr/bin/env python
from tkinter.tix import INTEGER
import GuiTextArea
import RouterPacket
import F
from copy import deepcopy

# formula bellman-ford:
#
# Dx(y) min{c(x,y) + Dy(y), c(x,z) + Dz(y)}
#


class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None
    distanceVector = None

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea(
            "  Output window for Router #" + str(ID) + "  ")
        self.costs = deepcopy(costs)

        # Initilizes the nodes as a Matrix with infinity distances to each other
        self.initDistanceVector()

        # Sends update packet if nodes are adjecent
        self.sendUpdate()

    # ---------------------------------------------------
    def initDistanceVector(self):
        self.distanceVector = [
            [0 for _ in range(self.sim.NUM_NODES)] for _ in range(self.sim.NUM_NODES)]

        for i in range(self.sim.NUM_NODES):
            for j in range(self.sim.NUM_NODES):
                if i == self.myID and j == self.myID:
                    self.distanceVector[i][j] = 0
                else:
                    self.distanceVector[i][j] = deepcopy(self.sim.INFINITY)

        # Initilizes the self nodes costs to neighbors
        self.distanceVector[self.myID] = deepcopy(self.costs)

    # ----------------------------------------------------
    def updateDistanceVector(self, mincost, sourceid=None):
        if sourceid == None:
            sourceid = deepcopy(INTEGER)
            sourceid = deepcopy(self.myID)

        for nodeID in range(0, self.sim.NUM_NODES):
            if self.distanceVector[sourceid][nodeID] < mincost[nodeID]:
                self.distanceVector[self.myID][nodeID] = deepcopy(self.costs[nodeID])
        
        self.distanceVector[sourceid] = deepcopy(mincost)

        for nodeID in range(self.sim.NUM_NODES):
            if not nodeID == self.myID:
                part_1 = self.distanceVector[self.myID][nodeID]
                part_2 = mincost[nodeID] + \
                    self.distanceVector[self.myID][sourceid]
                print("first calculation: " + str(part_1))
                print("second calculation: " + str(part_2))
                fastest = min(
                    self.distanceVector[self.myID][nodeID], mincost[nodeID] + self.distanceVector[self.myID][sourceid])
                self.distanceVector[self.myID][nodeID] = deepcopy(fastest)

    # ---------------------------------------------------
    def isAdjacent(self, nodeID):
        return nodeID != self.myID and self.costs[nodeID] != self.sim.INFINITY

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        print("node: " + str(self.myID) +
            " recieved packet from " + str(pkt.sourceid))
        print("-------------------------------------------")

        # Later check if any changes were made, in that case -> send packet to neighbours
        oldDistanceVector = deepcopy(self.distanceVector[self.myID])
        if not self.myID == pkt.sourceid:
            self.updateDistanceVector(
                deepcopy(pkt.mincost), deepcopy(pkt.sourceid))

        
        print("\nReceived:")
        print(pkt.mincost)
        print("My actual costs:")
        print(self.costs)
        print("Old:")
        print(oldDistanceVector)
        print("New:")
        print(self.distanceVector[self.myID])
        print("\n")
        if oldDistanceVector != self.distanceVector[self.myID]:
            print("CHANGED... sending packet")
            self.sendUpdate()

    # --------------------------------------------------
    def sendUpdate(self):
        for nodeID in range(0, self.sim.NUM_NODES):
            if self.isAdjacent(nodeID):
                print("at node: " + str(self.myID) +
                      ", sending to node: " + str(nodeID))
                pkt = RouterPacket.RouterPacket(
                    self.myID, nodeID, deepcopy(self.distanceVector[self.myID]))
                self.sim.toLayer2(pkt)
        print("----------------------------------")

    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        self.myGUI.println("")
        self.myGUI.println("Distancetable:")
        self.myGUI.print("      dst | ")
        for nodeID in range(0, self.sim.NUM_NODES):
            self.myGUI.print("   " + str(nodeID))
        self.myGUI.println("\n--------------------------")

        for rowNodeID in range(0, self.sim.NUM_NODES):
            self.myGUI.print(" nbr    " + str(rowNodeID) + " |    ")
            for colNodeID in range(0, self.sim.NUM_NODES):
                self.myGUI.print(
                    str(self.distanceVector[rowNodeID][colNodeID]) + "   ")
            self.myGUI.print("\n")

        self.myGUI.println("--------------------------")
        self.myGUI.print(" cost     |    ")
        for nodeID in range(0, self.sim.NUM_NODES):
            self.myGUI.print(
                str(self.costs[nodeID]) + "   ")
        self.myGUI.print("\n")

        self.myGUI.print(" distance |    ")
        for nodeID in range(0, self.sim.NUM_NODES):
            self.myGUI.print(
                str(self.distanceVector[self.myID][nodeID]) + "   ")
        self.myGUI.print("\n")
        self.myGUI.print("\n")

    # --------------------------------------------------

    def updateLinkCost(self, destID, newcost):
        pass
        # Update costs for self and distanceVector
        #self.costs[destID] = deepcopy(newcost)

        # If newcost is directly linked and smaller it should be then new fastest
        # if newcost < self.distanceVector[self.myID][destID]:
        #     self.distanceVector[self.myID][destID] = deepcopy(newcost)
        #     self.distanceVector[destID][self.myID] = deepcopy(newcost)
        #     self.sendUpdate()
        # else:
        #     self.distanceVector[destID][self.myID] = deepcopy(newcost)
        #     for nodeID in range(0, self.sim.NUM_NODES):
        #         if nodeID == destID: 
        #             self.distanceVector[self.myID][destID] = deepcopy(newcost)
        #         else:
        #             self.distanceVector[self.myID][destID] = self.sim.NUM_NODES
            #self.sendUpdate()
            # oldDistanceVector = deepcopy(self.distanceVector)
            # self.initDistanceVector()
            # for nodeID in range(0, self.sim.NUM_NODES):
            #     if nodeID != self.myID:
            #         pkt = RouterPacket.RouterPacket(
            #             nodeID, self.myID, deepcopy(oldDistanceVector[nodeID]))
            #         self.recvUpdate(pkt)
            # for nodeID in range(0, self.sim.NUM_NODES):
            #     if nodeID != self.myID:
            #         prevFast = self.sim.INFINITY
            #         fast = 0
            #         compare1 = self.costs[nodeID]
            #         for neighbor in range(0, self.sim.NUM_NODES):
            #             if neighbor != nodeID:
            #                 compare2 = self.distanceVector[neighbor][nodeID] + self.distanceVector[self.myID][neighbor]
            #                 fast = min(compare1, compare2)
            #                 if fast < prevFast:
            #                     prevFast = deepcopy(fast)
                        
            #         self.distanceVector[self.myID][nodeID] = deepcopy(prevFast)
