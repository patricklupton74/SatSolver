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

input = str(input("enter a CNF. "))

#parse input, split into array of arrays representing a CNF and its disjunctive clauses
cnf = parseCNF(input)

print(cnf)

