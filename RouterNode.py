#!/usr/bin/env python
from tkinter.tix import INTEGER
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
                if i == ID and j == ID:
                    self.distanceVector[i][j] = 0
                else:
                    self.distanceVector[i][j] = self.sim.INFINITY

        # Initilizes the self nodes costs to neighbors
        self.distanceVector[self.myID] = self.costs

        # Sends update packet if nodes are adjecent
        self.sendUpdate()

    # --------------------------------------------------
    def isAdjacent(self, nodeID):
        return nodeID != self.myID      # TODO: add "not equal to" infinity aswell later

    # ----------------------------------------------------
    def updateDistanceVector(self, mincost, sourceid = None):
        if sourceid == None:                   #<----The updateDistanceVector was called from the node itself
            sourceid = INTEGER                 #<----This line is to make sure sourceid becomes and integer (a hack)                        
            sourceid = self.myID               #If not sourceid == None, it gets it value from caller of the function

        self.distanceVector[sourceid] = mincost     #This should probably not affect the calculation below... fingers crossed.. 

        for nodeID in range(self.sim.NUM_NODES):
                self.distanceVector[self.myID][nodeID] = min(
                    self.costs[nodeID] + self.costs[self.myID], mincost[nodeID] + mincost[self.myID])
    
    # --------------------------------------------------
    def recvUpdate(self, pkt):
        print("node: " + str(self.myID) + " recieved packet from " + str(pkt.sourceid))
        print("-------------------------------------------")

        oldDistanceVector = deepcopy(self.distanceVector[self.myID])             #Later check if any changes were made, in that case -> send packet to neighbours
        if not self.myID == pkt.sourceid:
            self.updateDistanceVector(pkt.mincost, pkt.sourceid)
        
        print("\nOld:")
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
                print("at node: " + str(self.myID) + ", sendint to node: " + str(nodeID))
                pkt = RouterPacket.RouterPacket(self.myID, nodeID, self.distanceVector[self.myID])
                self.sim.toLayer2(pkt)

    # --------------------------------------------------

    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        self.myGUI.println("")
        self.myGUI.println("Distancetable:")
        self.myGUI.println("      dst |    0   1   2")
        self.myGUI.println("--------------------------")

        for nodeID in range(0, self.sim.NUM_NODES):
            self.myGUI.print(" nbr    " + str(nodeID) + " |    ")
            for i in range(0, self.sim.NUM_NODES):
                self.myGUI.print(str(self.distanceVector[nodeID][i]) + "   ")
            self.myGUI.print("\n")

    # --------------------------------------------------

    def updateLinkCost(self, destID, newcost):
        # Update costs for self and distanceVector
        self.costs[destID] = newcost
        self.updateDistanceVector(self.costs)
        # Send update to all adjencent nodes
        self.sendUpdate()

        pass
