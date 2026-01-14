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

def simplify(cnf, trues):
    #unit propagation (clauses with exactly 1 proposition must be true)
    #loop through cnf array of arrays (clauses), seeing if any clauses have only 1 proposition 
    for x in range(len(cnf)):
        if len(cnf[x]) == 1:
            #if trues already contains inverse of this clause then return contradiction
            if ((cnf[x][0]) * -1) in trues:
                return False
            else:
                trues.append((cnf[x][0]))
                #deals with new truth assignment
                for y in range(len(cnf)):
                    #if clause is depedent, make it empty
                    if cnf[x][0] in cnf[y]:
                        cnf[y] = []
                    #if clause has inverse, remove the inverse, leaving only other propositions in that clause
    #remove all empty clauses
    for x in range(len(cnf)):
        if cnf[len(cnf) - x - 1] == []:
            cnf.pop(len(cnf) - x - 1)
    return True

def DPLL(cnf):
    trues = []
    if simplify(cnf, trues):
        print(cnf)
        print(trues)
    else:
        print("unsat")
        print(cnf)
        print(trues)

DPLL(cnf)
    