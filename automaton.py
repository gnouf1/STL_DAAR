from typing import List


class NDFA:

    def __init__(self, tTab=[], eTab=[]) -> None:
        self.tTab = tTab
        self.eTab = eTab

    def __str__(self) -> str:
        res = "Initial state : 0\nFinal State :" + str(len(self.tTab)-1) + "\n"
        for i in range(0, len(self.eTab)):
            for s in self.eTab[i]:
                res += "  " + str(i) +" -- epsilon --> " + str(s) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + " --> " + str(self.tTab[i][col]) + "\n"

        return res


class DFA:
    def __init__(self, initialState: int = 0, finalStates: List = [], tTab=[]) -> None:
        self.initalState = initialState
        self.finalStates = finalStates
        self.tTab = tTab

    def __str__(self) -> str:
        res = "Initial state : " + str(self.initalState) + "\nFinal States :" + str(self.finalStates) + "\n"

        for i in range(0, len(self.tTab)):
            for col in range(0, 256):
                if(self.tTab[i][col] != -1):
                    res += "  " + str(i) + " -- " + chr(col) + " --> " + str(self.tTab[i][col]) + "\n"
        return res

    def goToMermaid(self):
        with open("DFA.txt", "w") as f:
            f.write("graph TD\n")

            for fs in self.finalStates:
                f.write("{0}[[{0}]]\n".format(fs))

            f.write("{0}(({0}))\n".format(self.initalState))

            for i in range(0, len(self.tTab)):
                for col in range(0, 256):
                    if(self.tTab[i][col] != -1):
                        f.write("  " + str(i) + " --> |" + chr(col) + "| " + str(self.tTab[i][col]) + "\n")

    # def checkString(self, str="") -> bool:
    #     if str == "":
    #         return False
    #
    #     for i in range(0, strLen):
    #         if str[i] ==

        strLen = len(str)
