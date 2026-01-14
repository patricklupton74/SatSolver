def parseClause(clauseString):
    clauseArray = []
    i = 0
    for x in range(len(clauseString)):
        if clauseString[x] == "∨":
            clauseArray.append(clauseString[i:x])
            i = x + 1
    clauseArray.append(clauseString[i:len(clauseString)])    
    return clauseArray

def parseCNF(input):
    cnf = []
    i = 0
    for x in range(len(input)):
        if input[x] == "∧":
            clauseString = input[i:x]
            i = x + 1
            cnf.append(parseClause(clauseString))
    cnf.append(parseClause(input[i:len(input)]))    
    return cnf

input = str(input("enter a CNF. "))

#parse input, split into array of arrays representing a CNF and its disjunctive clauses
cnf = parseCNF(input)

print(cnf)

