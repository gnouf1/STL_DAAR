from typing import List
from time import sleep
import copy
import utils as u


class NDFA:
    def __init__(self, tTab=[], eTab=[]) -> None:
        self.tTab = tTab
        self.eTab = eTab

    def __str__(self) -> str:
        res = "Initial state : 0\nFinal State :" + str(len(self.tTab)-1) + "\n"
        for i in range(0, len(self.eTab)):
            for s in self.eTab[i]:
                res += "  " + str(i) + " -- epsilon --> " + str(s) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + \
                                      " --> " + str(self.tTab[i][col]) + "\n"

        return res

    def __eq__(self, o: object) -> bool:
        if o == None:
            return False
        elif self.eTab != o.eTab:
            return False
        elif self.tTab != o.tTab:
            return False
        else:
            return True

    def goToMermaid(self):
        with open("NDFA.txt", "w") as f:
            f.write("graph TD\n")
            f.write("leg1((Init))\n")
            f.write("leg2[[Final]]\n")
            f.write("leg3[Transit state]\n")

            f.write("{0}[[{0}]]\n".format(len(self.tTab) - 1))

            f.write("{0}(({0}))\n".format(0))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col)
                                + "| " + str(self.tTab[i][col]) + "\n")

            for i in range(0, len(self.eTab)):
                for s in self.eTab[i]:
                    f.write("  " + str(i) + " --> |"
                            + 'epsilon' + "| " + str(s) + "\n")


class DFA:
    def __init__(self, initialState: int = 0, finalStates: List = [], tTab=[]) -> None:
        self.initialState = initialState
        self.finalStates = finalStates
        self.tTab = tTab
        self.sink = None
        self.lang = None

    def __str__(self) -> str:
        res = "Initial state : " + \
            str(self.initialState) + "\nFinal States :" + \
            str(self.finalStates) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + \
                                      " --> " + str(self.tTab[i][col]) + "\n"
        return res

    def __eq__(self, o: object) -> bool:
        if o == None:
            return False
        elif self.initialState != o.initialState:
            return False
        elif self.finalStates != o.finalStates:
            return False
        elif self.tTab != o.tTab:
            return False
        else:
            return True

    def getStates(self):
        """
        return dict
        ["noFinal"] = no final states
        ["final"] = final states
        """
        states = [x for x in range(0, len(self.tTab))
                  if x not in self.finalStates]
        res = dict()
        res["noFinal"] = states
        res["final"] = self.finalStates
        return res

    def getLang(self):
        if not self.lang:
            res = []
            for i in range(0, len(self.tTab)):
                tmp = [self.tTab[i].index(ele)
                       for ele in self.tTab[i] if ele != -1]
                if tmp:
                    res += [chr(ele) for ele in tmp if chr(ele) not in res]
            self.lang = res
            return res
        else:
            return self.lang

    def completeAutomaton(self):
        needed = False

        s = self.getStates()
        nestS = s["noFinal"]
        nestS += s["final"]

        for char in self.getLang():
            asciichar = ord(char)
            for i in nestS:
                if self.tTab[i][asciichar] == -1:
                    needed = True
                    break

        if not self.sink and needed:
            sink = len(self.tTab)
            self.sink = sink
            self.tTab.append([-1 for i in range(0, 256)])

            for char in self.getLang():
                asciichar = ord(char)
                for i in range(0, len(self.tTab)):
                    if self.tTab[i][asciichar] == -1:
                        self.tTab[i][asciichar] = sink

    def goToMermaid(self, fn=""):
        with open("DFA"+fn+".txt", "w") as f:
            f.write("graph TD\n")
            f.write("leg0[(Init & Final)]\n")
            f.write("leg1((Init))\n")
            f.write("leg2[[Final]]\n")
            f.write("leg3[Transit state]\n")

            for fs in self.finalStates:
                if fs == self.initialState:
                    f.write("{0}[({0})]\n".format(fs))
                elif fs != self.initialState:
                    f.write("{0}[[{0}]]\n".format(fs))

            if self.initialState not in self.finalStates:
                f.write("{0}(({0}))\n".format(self.initialState))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col)
                                + "| " + str(self.tTab[i][col]) + "\n")

    def getNextState(self, parentId: int):
        row = self.tTab[parentId]
        res = []

        for i in range(0, len(row)):
            if row[i] != -1:
                res.append(row[i])
        return res

    def getTransitionAtState(self, parentId):
        row = self.tTab[parentId]
        res = []
        for i in self.getLang():
            if row[ord(i)] != -1:
                res.append(i)
        return res

    def checkSubString(self, line="") -> bool:
        res = []
        strlen = len(line)
        rowlen = len(self.tTab[self.initialState])
        currentState = self.initialState
        i = 0
        wordStart = -1

        for c in line:
            asciiChar = ord(c)

            # Traitement exclusif des caractères ascii
            if asciiChar <= rowlen:
                next = self.tTab[currentState][asciiChar]

                if next != -1:
                    # Cas où on peut avancer dans l'automate
                    currentState = next
                    if wordStart == -1:
                        wordStart = i

                else:
                    if currentState in self.finalStates:
                        # Cas où on n'avance plus et c'est un état final
                        if wordStart != -1:
                            res.append((wordStart, i))

                    # Cas où on n'avance plus
                    if self.tTab[self.initialState][asciiChar] != -1:
                        # On vérifie que depuis l'état inital on puisse avancer
                        currentState = self.tTab[self.initialState][asciiChar]
                        wordStart = i

                    else:
                        currentState = self.initialState
                        wordStart = -1

            i += 1
        return res

    def checkString(self, inputString=""):
        ret = self.checkSubString(inputString)

        if ret:
            return ret
        else:
            return False

    def getListOfDeadStates(self) -> List:
        res = []

        s = self.getStates()

        nestS = []
        nestS += s["noFinal"]
        nestS += s["final"]

        for state in nestS:
            nbm1 = self.tTab[state].count(-1)
            nbself = self.tTab[state].count(state)

            if (nbm1 + nbself) >= len(self.tTab[state]) and state not in self.finalStates:
                res.append(state)

        return res

    def mini(self):
        self.completeAutomaton()
        s = self.getStates()

        nestS = []
        nestS += s["noFinal"]
        nestS += s["final"]

        descState = dict()
        lastBilan = dict()

        famID = 0
        for nfs in s["noFinal"]:
            descState[nfs] = [famID]
            lastBilan[nfs] = [famID]
        famID += 1
        for fs in s["final"]:
            descState[fs] = [famID]
            lastBilan[fs] = [famID]

        flag_continue = True
        i = 0

        # Algo de moore
        while flag_continue:
            currentBilan = dict()

            i += 1
            for state in nestS:
                for t in self.getLang():
                    nextState = self.tTab[state][ord(t)]
                    nsFamId = descState[nextState][0]
                    descState[state].append(nsFamId)
            idfam = 0
            for desc_0 in descState:
                for desc_1 in descState:
                    if descState[desc_0] == descState[desc_1]:
                        if desc_0 in currentBilan:
                            currentBilan[desc_1] = copy.deepcopy(currentBilan[desc_0])
                        else:
                            idfam += 1
                            currentBilan[desc_0] = [idfam]
                            currentBilan[desc_1] = [idfam]

            if currentBilan == lastBilan:
                flag_continue = False
            else:
                lastBilan = copy.deepcopy(currentBilan)
                descState = copy.deepcopy(currentBilan)

        # Suppression des états morts
        iterSec = 0
        while self.getListOfDeadStates() and iterSec <= len(nestS):
            iterSec += 1

            for deadState in self.getListOfDeadStates():
                del(self.tTab[deadState])
                del(currentBilan[deadState])

                nestS.remove(deadState)
                for state in nestS:
                    for asciichar in self.getLang():
                        if self.tTab[state][ord(asciichar)] == deadState:
                            self.tTab[state][ord(asciichar)] = -1
        currentBilan = u.reIndexDict(currentBilan)

        # Changement de l'état initial
        self.initialState = currentBilan[self.initialState][0]


        # Changement des états finaux
        oldFs = self.finalStates
        newFs = []

        for ofs in oldFs:
            s = currentBilan[ofs][0]
            if s not in newFs:
                newFs.append(s)

        self.finalStates = newFs

        # nouvelle matrice
        matrixCanva = dict()
        for e in currentBilan:
            newStateId = currentBilan[e][0]
            try:
                matrixCanva[newStateId].append(e)
            except KeyError:
                matrixCanva[newStateId] = [e]

        matrixCanvaRes = dict()
        i = 0
        for e in matrixCanva:
            i += 1
            matrixCanvaRes[i] = [e]

        matrixCanva = matrixCanvaRes

        newtTab = [[-1 for i in range(0, 256)] for j in range(0, len(matrixCanva)+1)]

        for state in nestS:
            for asciichar in self.getLang():
                tDest = self.tTab[state][ord(asciichar)]
                if tDest != -1:
                    newtTab[currentBilan[state][0]][ord(asciichar)] = currentBilan[tDest][0]

        self.tTab = newtTab
