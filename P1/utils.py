# class and global functions that use in main part of code
import random


class DFA:

    def __init__(self, states, transitions, startState, finalStates, alphabets):

        self.states = states
        self.transitions = transitions
        self.startState = startState
        self.finalStates = finalStates
        self.head = None
        self.alphabets = alphabets

    def SetHead(self, head):
        self.head = head

    def IsAcceptByDFA(self, inputString):

        startState = self.startState

        self.SetHead(startState)

        if inputString == "":
            if self.startState in self.finalStates:
                return True
            else:
                return False

        for character in inputString:

            for transition in self.transitions:
                if transition[0] == self.head and transition[1] == character:
                    self.SetHead(transition[2])
                    break

        if self.head in self.finalStates:
            return True
        else:
            return False

    def MakeSimpleDFA(self):

        noneFinalState = list()
        for state in self.states:
            if state not in self.finalStates:
                noneFinalState.append(state)

        noneFinalState.sort()
        self.finalStates.sort()

        stateStatus = list()
        stateStatus.append([noneFinalState, self.finalStates])

        while len(stateStatus) < 2 or stateStatus[-1] != stateStatus[-2]:

            transitionActions = list()
            lastStatesStatus = stateStatus[-1]

            for state in self.states:
                stateTransitionActions = list()
                for alphabet in self.alphabets:

                    for transition in self.transitions:
                        if transition[0] == state and transition[1] == alphabet:
                            nextState = transition[2]
                            break

                    for index in range(len(lastStatesStatus)):

                        if nextState in lastStatesStatus[index]:
                            stateTransitionActions.append(index)
                            break

                transitionActions.append([state, stateTransitionActions])

            haveSeenStates = list()
            newStateStatus = list()

            for item in transitionActions:
                if item[1] not in haveSeenStates:
                    haveSeenStates.append(item[1])
                    newStateStatus.append([item[0]])
                else:
                    index = haveSeenStates.index(item[1])
                    newStateStatus[index].append(item[0])

            stateStatus.append(newStateStatus)

        simpleDFAStates = stateStatus[-1]
        simpleDFAAlphabets = self.alphabets
        simpleDFATransition = list()

        for item in simpleDFAStates:

            state = item[0]
            for alphabet in self.alphabets:
                for transition in self.transitions:
                    if state == transition[0] and alphabet == transition[1]:
                        nextState = transition[2]
                        break
                for index in range(len(simpleDFAStates)):
                    if nextState in simpleDFAStates[index]:
                        nextState = simpleDFAStates[index]
                        break

                simpleDFATransition.append([item, alphabet, nextState])

        for item in simpleDFAStates:
            if self.startState in item:
                simpleDFAStartState = item
                break

        simpleDFAFinalStates = list()

        for item in simpleDFAStates:
            if item[0] in self.finalStates:
                simpleDFAFinalStates.append(item)

        simpleDFA = DFA(simpleDFAStates, simpleDFATransition, simpleDFAStartState, simpleDFAFinalStates, self.alphabets)
        return simpleDFA


class NFA():

    def __init__(self, states, finalStates, transitions, alphabets):
        self.states = states
        self.startState = states[0]
        self.alphabets = alphabets
        self.finalStates = finalStates
        self.headsList = list()
        self.transitions = transitions
        self.lamda = dict()
        for state in states:
            self.FindPathToLamdaTransition(state)

    def SetHead(self, headList):
        self.headsList = headList

    def FindPathToLamdaTransition(self, state):
        checkState = []
        possibleState = [state]
        for item in possibleState:
            if checkState == possibleState:
                break
            newStates = self.transitions[item + "_" + "lamda"]
            for newState in newStates:
                if newState not in possibleState:
                    possibleState.append(newState)
            checkState.append(item)
            self.lamda[state] = possibleState

    def IsAcceptByNFA(self, inputString):

        self.SetHead(self.lamda[self.startState])
        for character in inputString:
            updateHeadList = list()
            # is valid operation
            for item in self.headsList:
                newStates = self.transitions[item + "_" + character]
                for state in newStates:
                    if state not in updateHeadList:
                        updateHeadList.append(state)

            for item in updateHeadList:
                possibleState = self.lamda[item]
                for state in possibleState:
                    if state not in updateHeadList:
                        updateHeadList.append(state)

            self.SetHead(updateHeadList)
            if self.headsList == []:
                return False

        if inputString == "":
            self.SetHead(self.lamda[self.startState])

        for item in self.headsList:
            if item in self.finalStates:
                return True

        return False

    def CreateEqeulvantDFA(self):

        startStateList = self.lamda[self.startState]
        startStateList.sort()

        statesListForm = list()
        statesListForm.append(startStateList)

        states = list()

        transitions = list()

        for item in statesListForm:
            for alphabet in self.alphabets:
                newState = list()
                for state in item:
                    addStates = self.transitions[state + "_" + alphabet]
                    for innerState in addStates:
                        if innerState not in newState:
                            newState.append(innerState)

                for state in newState:
                    lamdaStates = self.lamda[state]
                    for innerState in lamdaStates:
                        if innerState not in newState:
                            newState.append(innerState)

                newState.sort()
                transition = (item, alphabet, newState)
                if newState != []:
                    transitions.append(transition)

                if newState not in statesListForm and newState != []:
                    statesListForm.append(newState)

        finalStates = list()

        NfaFinalStates = self.finalStates

        for item in statesListForm:
            for state in item:
                if state in NfaFinalStates:
                    finalStates.append(item)
                    break

        return DFA(statesListForm, transitions, startStateList, finalStates, self.alphabets)


class GNFA:

    def __init__(self, inputNFA):

        self.states = list()
        self.states.append("qstart")
        self.states.append("qend")
        self.states += inputNFA.states
        self.transitions = dict()
        self.alphabets = inputNFA.alphabets
        self.transitions["qstart_qend"] = "unkown"
        for state in inputNFA.states:

            if state == inputNFA.startState and state in inputNFA.finalStates:

                self.transitions["qstart" + "_" + state] = ""
                self.transitions[state + "_" + "qend"] = ""

            elif state == inputNFA.startState:

                self.transitions["qstart" + "_" + state] = ""
                self.transitions[state + "_" + "qend"] = "unkown"

            elif state in inputNFA.finalStates:

                self.transitions[state + "_" + "qend"] = ""
                self.transitions["qstart" + "_" + state] = "unkown"

            elif state != inputNFA.startState and state not in inputNFA.finalStates:

                self.transitions["qstart" + "_" + state] = "unkown"
                self.transitions[state + "_" + "qend"] = "unkown"

        for state in inputNFA.states:
            stateTotalTransition = list()
            for alphabet in self.alphabets + ["lamda"]:
                nextStates = inputNFA.transitions[state + "_" + alphabet]
                stateTotalTransition.append(nextStates)

            for state1 in inputNFA.states:
                transitionAlphabets = list()
                for index in range(len(stateTotalTransition) - 1):
                    if state1 in stateTotalTransition[index]:
                        transitionAlphabets.append(self.alphabets[index])

                if state == state1 and transitionAlphabets == []:

                    if state1 in stateTotalTransition[-1]:
                        self.transitions[state + "_" + state1] = ""
                    else:
                        self.transitions[state + "_" + state1] = "unkown"

                elif state == state1 and transitionAlphabets != []:

                    rejex = "("
                    for item in transitionAlphabets:
                        rejex += item + "+"

                    rejex = rejex[:len(rejex) - 1] + ")*"

                    self.transitions[state + "_" + state1] = rejex

                elif state != state1 and transitionAlphabets != []:

                    rejex = "("
                    for item in transitionAlphabets:
                        rejex += item + "+"

                    rejex = rejex[:len(rejex) - 1] + ")"

                    self.transitions[state + "_" + state1] = rejex

                elif state != state1 and transitionAlphabets == []:
                    if state1 in stateTotalTransition[-1]:
                        self.transitions[state + "_" + state1] = ""
                    else:
                        self.transitions[state + "_" + state1] = "unkown"

    def ReduceState(self):

        if len(self.states) == 2:
            return None

        ReduceOne = random.choice(self.states)
        while ReduceOne == "qend" or ReduceOne == "qstart":
            ReduceOne = random.choice(self.states)
        print("++++++")
        print(ReduceOne)
        newTransition = dict()
        newStates = self.states[0:self.states.index(ReduceOne)] + self.states[self.states.index(ReduceOne) + 1:]

        labelR2 = self.transitions[ReduceOne + "_" + ReduceOne]

        for state1 in newStates:
            if state1 == "qend":
                continue
            for state2 in newStates:
                if state2 == "qstart":
                    continue
                if state1 != state2:
                    labelR1 = self.transitions[state1 + "_" + ReduceOne]
                    labelR3 = self.transitions[ReduceOne + "_" + state2]
                    labelR4 = self.transitions[state1 + "_" + state2]

                    if labelR1 == "unkown" or labelR3 == "unkown":
                        newTransition[state1 + "_" + state2] = labelR4
                    else:
                        if labelR2 == "unkown" or labelR2 == "":
                            if labelR4 == "unkown" or labelR4 == "":
                                if labelR1 == "" and labelR3 == "":
                                    newTransition[state1 + "_" + state2] = ""
                                elif labelR1 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR3 + ")"
                                elif labelR3 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR1 + ")"
                                else:
                                    newTransition[state1 + "_" + state2] = "(" + labelR1 + labelR3 + ")"

                            else:
                                if labelR1 == "" and labelR3 == "":
                                    newTransition[state1 + "_" + state2] = labelR4
                                elif labelR1 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR3 + ")" + labelR4
                                elif labelR3 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR1 + ")" + labelR4
                                else:
                                    newTransition[state1 + "_" + state2] = "(" + labelR1 + labelR3 + ")" + labelR4

                        else:
                            if labelR4 == "unkown" or labelR4 == "":
                                if labelR1 == "" and labelR3 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR2 + ")*"
                                elif labelR1 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR2 + ")*(" + labelR3 + ")"
                                elif labelR3 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR1 + ")(" + labelR2 + ")*"
                                else:
                                    newTransition[
                                        state1 + "_" + state2] = "(" + labelR1 + ")(" + labelR2 + ")*(" + labelR3 + ")"
                            else:
                                if labelR1 == "" and labelR3 == "":
                                    newTransition[state1 + "_" + state2] = "(" + labelR2 + ")*+" + labelR4
                                elif labelR1 == "":
                                    newTransition[
                                        state1 + "_" + state2] = "(" + labelR2 + ")*(" + labelR3 + ")+" + labelR4
                                elif labelR3 == "":
                                    newTransition[
                                        state1 + "_" + state2] = "(" + labelR1 + ")(" + labelR2 + ")*+" + labelR4
                                else:
                                    newTransition[
                                        state1 + "_" + state2] = "(" + labelR1 + ")(" + labelR2 + ")*(" + labelR3 + ")+" + labelR4


                else:

                    if state1 != "qstart" and state1 != "qend":
                        newTransition[state1 + "_" + state2] = self.transitions[state1 + "_" + state2]

        self.states = newStates
        self.transitions = newTransition

        print(self.transitions)


def CreateNFA():
    states = input()
    states = states[1:len(states) - 1].split(",")

    alphabets = input()
    alphabets = alphabets[1:len(alphabets) - 1].split(",")

    transitionMapping = dict()
    for state in states:
        for alphabet in alphabets:
            transitionMapping[state + "_" + alphabet] = list()
        transitionMapping[state + "_" + "lamda"] = list()

    transitionCount = int(input())

    for count in range(transitionCount):
        transition = input()
        if transition[::-1][0] == ",":
            rule = transition.split(",")
            firstState = rule[0]
            nextState = rule[1]
            transitionMapping[firstState + "_" + "lamda"].append(nextState)
        else:
            firstState, nextState, sample = transition.split(",")
            transitionMapping[firstState + "_" + sample].append(nextState)

    finalStates = input()
    finalStates = finalStates[1:len(finalStates) - 1].split(",")

    testNFA = NFA(states, finalStates, transitionMapping, alphabets)
    return testNFA


def FindRejex(inputGNFA):
    while len(inputGNFA.states) > 2:
        inputGNFA.ReduceState()

    return inputGNFA.transitions["qstart_qend"]
