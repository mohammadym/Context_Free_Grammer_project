import copy
import random


class Grammer():
    
    def __init__(self,variables,terminals,rules):
        self.variables = variables
        self.terminals = terminals
        self.rules = rules # rules type is [[left hand],[right hand]]  A -> BC  [['A'],['B','C']] 
        self.startVariable = self.variables[0]
        self.variables.sort()
        self.terminals.sort()
        self.fullTerminalVariables = list()
        self.canReachVariables = list()
        self.isChomskyForm = 1
        self.isGreibachForm = 1
        self.isDeleteTrash = 1
        #check Chomsky form
        for item in self.rules:

            if len(item[1]) == 2:
                for variable in item[1]:
                    if not variable.isupper():
                        self.isChomskyForm = 0
                        break

            elif len(item[1]) == 1:
                if item[1][0] == 'lamda' and item[0][0] != self.startVariable:
                    self.isChomskyForm = 0
                    break

                elif item[1][0].isupper():
                    self.isChomskyForm = 0
                    break
            
            else:
                self.isChomskyForm = 0
                break
            
            if self.isChomskyForm == 0:
                break
        
        # check Geribach form

        for item in self.rules:
            
            if len(item[1]) == 1 and item[1][0] == 'lamda' and item[0][0] != self.startVariable:
                self.isGreibachForm = 0
                break

            else:
                for index in range(len(item[1])):
                    if index == 0 and item[1][index].isupper():
                        self.isGreibachForm = 0
                        break
                    elif index != 0 and item[1][index].islower():
                        self.isGreibachForm = 0 
                        break
                if self.isGreibachForm == 0:
                    break
        
        # check form is delete 

        for item in self.rules:
            if len(item[1]) == 1 and item[1][0].isupper():
                self.isDeleteTrash = 0
                break
            elif len(item[1]) == 1 and item[1][0] == 'lamda' and item[0][0] != self.startVariable:
                self.isDeleteTrash = 0
                break

        self.FindCanFullTerminalVariables()
        if self.FindCanFullTerminalVariables != self.variables:
            self.isDeleteTrash = 0
        self.CanReachVariables()
        if self.canReachVariables != self.variables :
            self.isDeleteTrash = 0
        
        
    def FindCanFullTerminalVariables(self):
        fullTerminalVariables = list()
        currentVariables = list()
        allowedliteral = self.terminals.copy()
        for item in rules:
            rulesTerminal = True
            for String in item[1]:
                if String not in  allowedliteral:
                    rulesTerminal = False
                    break
            if rulesTerminal:
                if item[0][0] not in currentVariables:
                    currentVariables.append(item[0][0])

        while currentVariables != fullTerminalVariables:
            for item in currentVariables : 
                if item not in allowedliteral:
                    allowedliteral.append(item)
            fullTerminalVariables += currentVariables
            for item in rules:
                rulesTerminal = True
                for String in item[1]:
                    if String not in allowedliteral:
                        rulesTerminal = False
                        break
                if rulesTerminal :
                    if item[0][0] not in currentVariables:
                        currentVariables.append(item[0][0])
            currentVariables.sort()
            fullTerminalVariables.sort()
        
        self.fullTerminalVariables = fullTerminalVariables.sort()


    def CanReachVariables(self):
        CanReachVariablesList = list()
        CanReachVariables.append(self.startVariable)
        for rule in self.rules:
            for String in rule[1]:
                if String in self.variables and String not in CanReachVariablesList:
                    CanReachVariablesList.append(String)
        
        CanReachVariablesList.sort()
        self.canReachVariables = CanReachVariablesList
    

    def RemoveLandaTransition(self,variable,rules):
        finalRules = rules.copy()
        for item in finalrule:
            newRules = [item]
            for rule in newRules : 
                for index in range(rule[1]):
                    if rule[1][index] == variable:
                        if rule[1][:index] + rule[1][index+1:] != []:
                            newRule = [[rule[0][0]],rule[1][:index] + rule[1][index+1:]]
                            if newRule not in newRules:
                                newRules.append(newRule)
            
            for rule in newRules:
                if rule not in finalRules:
                    finalRules.append(rule)
        lamdaVariableIndex = finalRules.index([[variable],['lamda']])
        finalRules = finalRules[0:lamdaVariableIndex] + finalRules[lamdaVariableIndex+1:]
        return finalRules


    def RemoveUnitProduction(self,variable1,variable2,rules):
        # we have rule variable1 -> variable2 in rules
        finalRules = rules.copy()
        for item in finalRules:
            newRules = [item]
            for rule in newRules:
                for index in range(len(rule[1])):
                    if rule[1][index] == variable1:
                        newRule = [[rule[0][0]],rule[:index] + [variable2] + rule[index+1:]]
                        if newRule not in newRules:
                            newRules.append(newRule)
            
            for item in newRules:
                if item not in finalRules:
                    finalRules.append(item)
            
        index = finalRules.index([[variable1],[variable2]])

        finalRules = finalRules[:index] + finalRules[index+1:]

        return finalRules



    def DeleteTrash(self):
        
        if isDeleteTrash == 0:
            #removing lamda transition
            finalRules = self.rules.copy()
            for item in finalRules:
                if item[1][0] == 'lamda':
                    finalAdditionRules = self.RemoveLandaTransition(item[0][0],finalRules)
                    for newRule in finalAdditionRules:
                        if newRule not in finalRules:
                            finalRules.append(newRules)
        
            #removing unit production

            for item in finalRules:
                if len(item[1]) == 1 and item[1][0].isupper():
                    finalAdditionRules = self.RemoveUnitProduction(item[0][0],item[1][0],finalRules)
                    for newRule in finalAdditionRules:
                        if newRule not in finalRules:
                            newRules.append(newRule)
        
            #removing useless production

            allowedliteral = self.terminals.copy()
            variables = []
            terminals = []
            for item in self.CanReachVariables:
                if item in self.fullTerminalVariables:
                    allowedliteral.append(item)
                    variables.append(item)
            if self.startVariable in terminals:
                index = terminals.index(self.startVariable)
                variables = [self.startVariable] + variables[:index] + variables[index+1:]
            
            trueFinalRules = list()
            for rule in finalRules:
                usefullRule = 1
                for index in range(2):
                    if usefullRule == 0:
                        break
                    for item in rule[index]:
                        if item not in allowedliteral:
                            usefullRule = 0
                            break
                    
                if usefullRule == 1:
                    trueFinalRules.append(rule)
            
            for rule in trueFinalRules:
                for item in rule[1]:
                    if item.islower() and item not in terminals:
                        terminals.append(item)

       
            newGrammerRule = trueFinalRules
            newGrammerVariable = variables
            newGrammerTerminals = terminals
        
            return Grammer(newGrammerVariable,newGrammerTerminals,newGrammerRule)
        else:
            print("this grammer have no problem")
    
    def ChangeToChomskyFrom(self):

        if self.isDeleteTrash == 1 and self.isChomskyForm == 0 :
            chomskyVariables = self.variables.copy()
            chomskyTerminals = self.terminals.copy()
            newRules = list()

            for rule in self.rules:
                backup = rule.copy()
                if len(backup[1]) == 1:
                    newRules.append(rule)
                else:
                    for index in range(len(backup[1])):
                        if backup[1][index].islower():
                            newVariable = self.MakeNewVariableName()
                            while newVariable in chomskyVariables:
                                newVariable = self.MakeNewVariableName()
                            newRule = [[newVariable],[backup[1][index]]]
                            if newRule not in newRules:
                                newRules.append(newRule)
                                chomskyVariables.append(newVariable)
                            backup[1][index] = newVariable

                    lastVariable = None   
                    for index in range(len(backup[1])-1):
                        newVariable = self.MakeNewVariableName()
                        while newVariable in chomskyVariables:
                            newVariable = self.MakeNewVariableName()
                        
                        if index == 0 :
                            newRule = [rule[0][0],[rule[1][0],newVariable]]
                            if newRule not in newRules:
                                newRules.append(newRule)
                            lastVariable = newVariable
                        elif index == len(backup[1]) - 2:
                            newRule = [[lastVariable],[backup[1][index],backup[1][index+1]]]
                            if newRule not in newRules:
                                newRules.append(newRule)
                        else:                            
                            newRule = [[lastVariable],[backup[1][index],newVariable]]
                            if newRule not in newRules:
                                newRules.append(newRule)
                            lastVariable = newVariable
            return Grammer(chomskyVariables,chomskyTerminals,newRules)

        elif self.isChomskyForm == 0 and self.isDeleteTrash == 0 :
            usefullGrammer = self.DeleteTrash()
            return usefullGramer.ChangeToChomskyFrom()
        
        elif self.isChomskyForm == 1:
            return self
        
    
    
    def ChangeToGreibachForm(self):
        
        if self.isGreibachForm == 0 and self.isDeleteTrash == 1:
            geribachVariables = self.variables.copy()
            geribachTerminals = self.terminals.copy()
            newRules = list()
            for rule in self.rules:
                if len(rule[1]) == 1:
                    newRules.append(rule)
                else:
                    #holy fuching shit man too hard
                    #fucking pass for today
                    pass
            

    def MakeNewVariableName(self):
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        randomNumber = random.randint(4,14)
        newVariable = ""
        for count in range(randomNumber):
            newVariable += random.choose(alphabet)
        return newVariable
           
            