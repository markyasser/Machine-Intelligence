from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        
        # Add the variables to the problem
        unique_chars = set(LHS0 + LHS1 + RHS)
        carries = set()
        for i in range(len(RHS) - 1):
            carries.add(f"C{i}")

        carries = list(carries)
        problem.variables = list(unique_chars) + carries


        # Add the domains to the problem
        last_digits = set(LHS0[0] + LHS1[0] + RHS[0])
        for char in unique_chars:
            if char in last_digits:
                problem.domains[char] = set(range(1, 10))
            else:
                problem.domains[char] = set(range(10))
        for carry in carries:
            problem.domains[carry] = set(range(2))


        # Add the constraints to the problem
        # 1 - All Different Binary Constraint
        for var1 in unique_chars:
            for var2 in unique_chars:
                if var1 == var2:
                    continue
                problem.constraints.append(BinaryConstraint((var1, var2), lambda x, y: x != y))

        LHS0 = LHS0[::-1]
        LHS1 = LHS1[::-1]
        RHS = RHS[::-1]
        
        # Loop on the RHS from the end to the start
        for i in range(len(RHS)):
            #-----------------------First column-----------------------
            if i == 0:
                # Add Auxiliary Variables
                aux1, aux2 = (LHS0[i], LHS1[i]), (RHS[i], carries[i])
                problem.variables.append(aux1)
                problem.variables.append(aux2)

                # Domain
                dom=set()
                for x in problem.domains[LHS0[i]]:
                    for y in problem.domains[LHS1[i]]:
                        dom.add((x,y))
                problem.domains[aux1] = dom
                dom=set()
                for x in problem.domains[RHS[i]]:
                    for y in problem.domains[carries[i]]:
                        dom.add((x,y))
                problem.domains[aux2] = dom

                # 2 - Constrain : A + B = C + 10 * C1
                problem.constraints.append(BinaryConstraint((LHS0[i], aux1), lambda a, b: a == b[0]))
                problem.constraints.append(BinaryConstraint((LHS1[i], aux1), lambda a, b: a == b[1]))
                problem.constraints.append(BinaryConstraint((RHS[i], aux2), lambda a, b: a == b[0]))
                problem.constraints.append(BinaryConstraint((carries[i], aux2), lambda a, b: a == b[1]))
                problem.constraints.append(BinaryConstraint((aux1, aux2), lambda a, b: a[0] + a[1]  == b[0] + 10 * b[1]))
            #-----------------------Last column-----------------------
            elif i == len(RHS) - 1:
                if i < len(LHS0) and i < len(LHS1): # Both LHS have the same length
                    # Add Auxiliary Variables
                    aux1 = (LHS0[i], LHS1[i], carries[i - 1])
                    problem.variables.append(aux1) 

                    # Domain
                    dom=set()
                    for x in problem.domains[LHS0[i]]:
                        for y in problem.domains[LHS1[i]]:
                            for z in problem.domains[carries[i - 1]]:
                                    dom.add((x,y,z))
                    problem.domains[aux1] = dom

                    # 3 - Constrain : A + B + C1 = C 
                    problem.constraints.append(BinaryConstraint((LHS0[i], aux1), lambda a, b: a == b[0]))
                    problem.constraints.append(BinaryConstraint((LHS1[i], aux1), lambda a, b: a == b[1]))
                    problem.constraints.append(BinaryConstraint((carries[i-1], aux1), lambda a, b: a == b[2]))
                    problem.constraints.append(BinaryConstraint((aux1, RHS[i]), lambda a, b: a[0] + a[1] + a[2] == b))

                elif i < len(LHS0) and i >= len(LHS1): # LHS0 is longer than LHS1
                    # Add Auxiliary Variables
                    aux1 = (LHS0[i], carries[i - 1])
                    problem.variables.append(aux1)

                    # Domain
                    dom=set()
                    for x in problem.domains[LHS0[i]]:
                        for z in problem.domains[carries[i - 1]]:
                            dom.add((x,z))
                    problem.domains[aux1] = dom

                    # 4 - Constrain : A + C1 = C
                    problem.constraints.append(BinaryConstraint((LHS0[i], aux1), lambda a, b: a == b[0]))
                    problem.constraints.append(BinaryConstraint((carries[i-1], aux1), lambda a, b: a == b[1]))
                    problem.constraints.append(BinaryConstraint((aux1, RHS[i]), lambda a, b: a[0] + a[1] == b)) 
                
                elif i >= len(LHS0) and i < len(LHS1): # LHS1 is longer than LHS0
                    # Add Auxiliary Variables
                    aux1 = (LHS1[i], carries[i - 1])
                    problem.variables.append(aux1)

                    # Domain
                    dom=set()
                    for x in problem.domains[LHS1[i]]:
                        for z in problem.domains[carries[i - 1]]:
                            dom.add((x,z))
                    problem.domains[aux1] = dom

                    # 5 - Constrain : B + C1 = C
                    problem.constraints.append(BinaryConstraint((LHS1[i], aux1), lambda a, b: a == b[0]))
                    problem.constraints.append(BinaryConstraint((carries[i-1], aux1), lambda a, b: a == b[1]))
                    problem.constraints.append(BinaryConstraint((aux1, RHS[i]), lambda a, b: a[0] + a[1] == b))

                elif i >= len(LHS0) and i >= len(LHS1): # Both LHS are shorter than RHS
                    # 6 - Constrain : C1 = C
                    problem.constraints.append(BinaryConstraint((carries[i-1], RHS[i]), lambda a, b: a == b))
            #-----------------------Middle columns-----------------------
            else: 
                if i < len(LHS0) and i < len(LHS1):
                    # Add Auxiliary Variables
                    aux1 = (LHS0[i], LHS1[i], carries[i - 1])
                    aux2 = (RHS[i], carries[i])

                    problem.variables.append(aux1) 
                    problem.variables.append(aux2) 

                    # Domain
                    dom=set()
                    for x in problem.domains[LHS0[i]]:
                        for y in problem.domains[LHS1[i]]:
                            for z in problem.domains[carries[i - 1]]:
                                dom.add((x,y,z))
                    problem.domains[aux1] = dom
                    dom=set()
                    for x in problem.domains[RHS[i]]:
                        for y in problem.domains[carries[i]]:
                            dom.add((x,y))
                    problem.domains[aux2] = dom
 
                    # 7 - Constrain : A + B + C1 = C + 10 C2
                    problem.constraints.append(BinaryConstraint((LHS0[i],aux1), lambda a, b: a == b[0])) 
                    problem.constraints.append(BinaryConstraint((LHS1[i],aux1), lambda a, b: a == b[1])) 
                    problem.constraints.append(BinaryConstraint((carries[i-1],aux1), lambda a, b: a == b[2])) 
                    problem.constraints.append(BinaryConstraint((RHS[i],aux2), lambda a, b: a  == b[0]))
                    problem.constraints.append(BinaryConstraint((carries[i],aux2), lambda a, b: a  == b[1])) 
                    problem.constraints.append(BinaryConstraint((aux1,aux2), lambda a, b: a[0] + a[1] + a[2] == b[0] + 10 * b[1]))
                
                else:
                    if i < len(LHS0) and i>=len(LHS1):
                        # Add Auxiliary Variables
                        aux1 = (LHS0[i] , carries[i - 1])
                        aux2 = (RHS[i] , carries[i])

                        problem.variables.append(aux1)
                        problem.variables.append(aux2) 

                        # Domain
                        dom=set()
                        for x in problem.domains[LHS0[i]]:
                            for y in problem.domains[carries[i-1]]:
                                dom.add((x,y))
                        problem.domains[aux1] = dom
                        dom=set()
                        for x in problem.domains[RHS[i]]:
                            for y in problem.domains[carries[i]]:
                                dom.add((x,y))
                        problem.domains[aux2] = dom

                        # 8 - Constrain : A + C1 = C + 10 C2
                        problem.constraints.append(BinaryConstraint((LHS0[i],aux1), lambda a, b: a == b[0]))

                        

                    elif i >= len(LHS0) and i<len(LHS1):
                        # Add Auxiliary Variables
                        aux1 = (LHS1[i] , carries[i - 1])
                        aux2 = (RHS[i] , carries[i])

                        problem.variables.append(aux1)
                        problem.variables.append(aux2) 

                        # Domain
                        dom=set()
                        for x in problem.domains[LHS1[i]]:
                            for y in problem.domains[carries[i-1]]:
                                dom.add((x,y))
                        problem.domains[aux1] = dom
                        dom=set()
                        for x in problem.domains[RHS[i]]:
                            for y in problem.domains[carries[i]]:
                                dom.add((x,y))
                        problem.domains[aux2] = dom

                        # 9 - Constrain : B + C1 = C + 10 C2
                        problem.constraints.append(BinaryConstraint((LHS1[i],aux1), lambda a, b: a == b[0]))

                    problem.constraints.append(BinaryConstraint((carries[i - 1],aux1), lambda a, b: a == b[1]))
                    problem.constraints.append(BinaryConstraint((RHS[i],aux2), lambda a, b: a == b[0]))
                    problem.constraints.append(BinaryConstraint((carries[i],aux2), lambda a, b: a == b[1]))
                    problem.constraints.append(BinaryConstraint((aux1,aux2), lambda a, b: a[0] + a[1]  == b[0] + 10 * b[1]))
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())