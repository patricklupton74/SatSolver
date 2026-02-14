####################### (↓) INPUT PARSING & SANITATION #######################

def lettersToNumbers(cnf):
    #loops through cnf array of arrays
    for x in range(len(cnf)):
        #loops through arrays inside array of arrays
        for y in range(len(cnf[x])):
            #if first character of an element in array inside array of arrays is '¬', multiply number by -1
            #else just display corresponding number to letter
            if ((cnf[x])[y])[0] == "¬":
                (cnf[x])[y] = str((ord(((cnf[x])[y])[1]) - ord('A') + 1) * -1)
            else:
                (cnf[x])[y] = str(ord((cnf[x])[y]) - ord('A') + 1)

def parseClause(clauseString):
    #intialises variable to hold output
    clauseArray = []
    i = 0
    #loops through input, splitting the string into an array holding each proposition, and eliminating '∨'
    for x in range(len(clauseString)):
        if clauseString[x] == "∨":
            clauseArray.append(clauseString[i:x])
            i = x + 1
    clauseArray.append(clauseString[i:len(clauseString)])    
    return clauseArray

def parseCNF(input):
    #removes spaces and brackets from input
    input = input.replace(" ", "")
    input = input.replace("(", "")
    input = input.replace(")", "")
    #initialises variable to hold output
    cnf = []
    i = 0
    #loops through input, splitting into clauses (held in strings)
    for x in range(len(input)):
        if input[x] == "∧":
            clauseString = input[i:x]
            i = x + 1
            #parseClause function turns clauses held in strings to clauses held as arrays of elements
            cnf.append(parseClause(clauseString))
    #ensures final clause is added too
    cnf.append(parseClause(input[i:len(input)]))  
    #turns letters to numbers e.g. A -> 1, B -> 2. '¬' is represented by -, e.g. ¬C -> -3
    lettersToNumbers(cnf)  
    return cnf

####################### (↑) INPUT PARSING & SANITATION #######################

input = str(input("enter a CNF. "))

#parse input, split into array of arrays representing a CNF and its disjunctive clauses
cnf = parseCNF(input)

print(cnf)

##not working unit propagation attempt 1.
# def simplify(cnf, trues):
#     #unit propagation (clauses with exactly 1 proposition must be true)
#     #loop through cnf array of arrays (clauses), seeing if any clauses have only 1 proposition 
#     for x in range(len(cnf)):
#         if len(cnf[x]) == 1:
#             #if trues already contains inverse of this clause then return contradiction
#             if ((cnf[x][0]) * -1) in trues:
#                 return False
#             else:
#                 trues.append((cnf[x][0]))
#                 #deals with new truth assignment
#                 for y in range(len(cnf)):
#                     #if clause is depedent, make it empty
#                     if cnf[x][0] in cnf[y]:
#                         cnf[y] = []
#                     #if clause has inverse, remove the inverse, leaving only other propositions in that clause
#     #remove all empty clauses
#     for x in range(len(cnf)):
#         if cnf[len(cnf) - x - 1] == []:
#             cnf.pop(len(cnf) - x - 1)
#     return True

# def DPLL(cnf):
#     trues = []
#     if simplify(cnf, trues):
#         print(cnf)
#         print(trues)
#     else:
#         print("unsat")
#         print(cnf)
#         print(trues)

# DPLL(cnf)

# plan for future: loop through list, finding all unit clauses, add to truth,
# check if negation already in truth, if so return contradiction
# remove all unti clauses, clauses dependent on the content of them and remove remove negations from other clauses
# continue to do this until all until all unit clauses are removed (new ones may be made by removing negations)
# if contradiction is found at this stage, then unsat as no branching can fix it (i think?)


def negation(truth):
    #removes - if already negated, adds - if not already negated
    if truth[0] == "-":
        return truth[1:]
    else:
        return "-" + truth

def removeUnitClauses(cnf, trues):
    #removes all unit clauses which have been found true so far
    newCnf = []
    for clause in cnf:
        clauseTrue = False
        for prop in clause:
            if prop in trues:
                clauseTrue = True
                break
        if not clauseTrue:
            newCnf.append(clause)
    return newCnf

def removeUnitNegations(cnf, trues):
    #removes the negations of all true propositions in clauses
    newCnf = []
    for clause in cnf:
        newClause = clause.copy()
        for truth in trues:
            if negation(truth) in newClause:
                newClause.remove(negation(truth))
        if len(newClause) == 0:
            return False
        newCnf.append(newClause)
    return newCnf



def unitPropagation(cnf, trues):
    #unit propagation -> process of setting all unit clauses (clauses with only 1 proposition) to true
    #if it is found that both a proposition and its negated form are present, it is UNSAT (returns false)
    #when a unit clause is set to true, all clauses the unit appears in are removed from the cnf
    #all negated units are removed from clauses
    #new unit clauses may be made by this last step, so the process needs to be repeated a number of times
    foundUnit = True 
    while foundUnit:
        foundUnit = False
        for x in range(len(cnf)):
            if len(cnf[x]) == 1:
                if (negation(cnf[x][0])) in trues:
                    return False
                elif cnf[x][0] not in trues:
                    trues.append(cnf[x][0])
                    foundUnit = True
        #updates cnf, before trying to find unit clauses more after removal of negations
        cnf = removeUnitClauses(cnf, trues)
        cnf = removeUnitNegations(cnf, trues)
        if cnf is False:
            return False
    return cnf

def pureLiteralElimination(cnf, trues):
    positives = set()
    negatives = set()
    #adds all positive clauses to postive set and all negative clauses to negative set
    for clause in cnf:
        for literal in clause:
            if literal[0] == "-":
                negatives.add(literal[1:])
            else:
                positives.add(literal[0])
    #creates sets of literals which only appear positive/negative
    purePositives = positives - negatives
    pureNegatives = negatives - positives
    #compiles into pure literal set (to be removed from cnf)
    pureLiterals = []
    for x in purePositives:
        pureLiterals.append(x)
    for x in pureNegatives:
        pureLiterals.append("-" + x)
    if not pureLiterals:
        return cnf
    #add pure literals to trues
    trues.extend(pureLiterals)
    #remove true literals from cnf (if any literal in a clause is pure, the clause is removed from the cnf)
    newCnf = []
    for clause in cnf:
        clauseSat = False
        for literal in clause:
            if literal in pureLiterals:
                clauseSat = True
                break
        if not clauseSat:
            newCnf.append(clause)
    return newCnf
    


        

trues = []
result = unitPropagation(cnf, trues)
#print(trues)

if result is False:
    print("UNSAT")
else:
    result = pureLiteralElimination(result, trues)    
    print("assignments:", trues)
    if len(result) == 0:
        print("SAT")
        print("final CNF:", result)
    else:
        #dpll & recurse
        print("after unit propagation and pure literal elimination, remaining CNF:")
        print(result)
    
#NEXT STEPS:
#ADD NEGATE HELPER, BECAUSE ADDING - INFRONT WONT WORK FOR DOUBLE NEGATIONS, done
#REMOVEUNITNEGATIONS SHOULD DETECT EMPTY CLAUSES, AND RETURN FALSE FOR UNSAT, done
#FIX UNIT PROPAGATION TO HABDLE POSSIBLE FALSE, done?
#FIX FINAL SAT/UNSAT PRINT LOGIC I.E. RETURNING FALSE/TRUE FROM FUNCTIONS, done





    