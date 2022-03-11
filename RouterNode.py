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
    nodeDestination = None
    count = None

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea(
            "  Output window for Router #" + str(ID) + "  ")
        self.costs = deepcopy(costs)
        self.nodeDestination = [0 for _ in range(self.sim.NUM_NODES)]
        self.nodeDestination[self.myID] = self.myID
        # Initilizes the nodes as a Matrix with infinity distances to each other
        self.initDistanceVector()

        # Sends update packet 
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

        # If packet comes from myself, there is no information to take from mincost
        if sourceid != self.myID:
            self.distanceVector[sourceid] = deepcopy(mincost)

        # Iterate through all neighbor nodes
        for toNode in range(0, self.sim.NUM_NODES):
            if self.myID != toNode:
                # If posioned reverse is active
                # This part makes sure to calculate the fastest route from self -> toNode
                # that is available right now. It also saves what adjacent node it uses as a first
                # step to get to the destination.  
                if self.sim.POISONREVERSE:
                    routes = {}
                    for nextHop in range(0, self.sim.NUM_NODES):
                        if nextHop != self.myID:
                            distanceToNode = self.costs[nextHop] + \
                                self.distanceVector[nextHop][toNode]
                            routes[nextHop] = deepcopy(distanceToNode)
                    
                    fastest = deepcopy(self.sim.INFINITY)    
                    for nextHop in routes:
                        if routes[nextHop] < fastest:
                            fastest = deepcopy(routes[nextHop])
                    for nextHop in routes:
                        if routes[nextHop] == fastest:
                            self.nodeDestination[toNode] = nextHop
                    self.distanceVector[self.myID][toNode] = deepcopy(
                        fastest)
                # If not poisoned
                # This version simply does not save the information of what adjacent node to get to destination    
                else:
                    routes = []
                    for nextHop in range(0, self.sim.NUM_NODES):
                        if nextHop != self.myID:
                            distanceToNode = self.costs[nextHop] + \
                                self.distanceVector[nextHop][toNode]
                            routes.append(distanceToNode)
                    self.distanceVector[self.myID][toNode] = deepcopy(
                        min(routes))
    # ---------------------------------------------------
    def isAdjacent(self, nodeID):
        return nodeID != self.myID and self.costs[nodeID] != self.sim.INFINITY

    # --------------------------------------------------
    def recvUpdate(self, pkt):
        oldDistanceVector = deepcopy(self.distanceVector[self.myID])
        if not self.myID == pkt.sourceid:
            self.updateDistanceVector(
                deepcopy(pkt.mincost), deepcopy(pkt.sourceid))

        if oldDistanceVector != self.distanceVector[self.myID]:
            self.sendUpdate()

    # --------------------------------------------------
    # send packet to adjacent 
    def sendUpdate(self):
        for nodeID in range(0, self.sim.NUM_NODES):
            if self.isAdjacent(nodeID):
                # If poisoned reverse is active
                if self.sim.POISONREVERSE:
                    fakeDistanceVector = deepcopy(self.distanceVector)
                    # If the destination routes through another node:
                    # send the distance as infinity to the destionation
                    for dest in range(0, len(self.nodeDestination)):
                        if nodeID == self.nodeDestination[dest]:
                            fakeDistanceVector[self.myID][dest] = self.sim.INFINITY
                    
                    pkt = RouterPacket.RouterPacket(
                        self.myID, nodeID, deepcopy(fakeDistanceVector[self.myID]))
                    self.sim.toLayer2(pkt)
                # If not poisoned 
                else:
                    pkt = RouterPacket.RouterPacket(
                        self.myID, nodeID, deepcopy(self.distanceVector[self.myID]))
                    self.sim.toLayer2(pkt)

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
        # Update costs for self and distanceVector
        self.costs[destID] = deepcopy(newcost)
        self.updateDistanceVector(self.costs, self.myID)
        self.sendUpdate()
