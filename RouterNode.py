#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

    # Node 0: 0 4 1
    # mincosts[] = {0, 5, 1}
    # Node 1: 4 0 50

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")
        self.costs = deepcopy(costs)


    # --------------------------------------------------
    def recvUpdate(self, pkt):
        if not self.myID == pkt.sourceid:
            pass
            # self.costs[pkt.sourceid] = pkt.mincosts[self.myID]

    # --------------------------------------------------
    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) + "  at time " + str(self.sim.getClocktime()))
        self.myGUI.println("")
        self.myGUI.println("Distancetable:")
        self.myGUI.println("      dst |    0   1   2")
        self.myGUI.println("--------------------------")
        self.myGUI.print(" nbr    " + str(self.myID) + " |    " + str(self.costs[0]) + "   " + 
                                        str(self.costs[1]) + "   " + str(self.costs[2]) + "\n")


    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        pass
