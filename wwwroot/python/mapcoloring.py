from itertools import product 
import math

class MapColorer:

    def initializeDomains(self) :
        """
            1) initialize the domain, Di, for each variable i in graph to the set of colors
            
            we will use a dictionary with key = state-name and values = available-colors
        """
        """pseudo code
        for each key in adj_dict.keys {
            domain_dict.add(key)    
            for each color in colors {
                domain_dict[key].add(color)
            }
        }     
        """
        for state in self.adj_dict :
            self.domains_dict[state] = []
            for color in self.colors :
                self.domains_dict[state].append(color)
            
        #print(f"DOMAIN DICT: {self.domains_dict}")

    def initializeConstraints(self) :
        """
            the constraints for this assignment are defined as:
                no adjacent states can have the same colors

            2) initialize the constraints for each variable Xk
                a) for Xi in Xk.adjacencies, create constraint
                    - Cki ({Xk,Xi}, {Rk})
                b) Relation Rk is cartesian product of Dk and Di
                    -filter matching : Rk = {(x,y) in Dk X Di such that x != y}

            -we will use a dictionary with key = state-name and value = [{ Skj0, { (c1, c2), (c2, 1) ...} }]
            -so it will be a dictionary of list of pairs for that key, each pair containing the scope and the cartesian product of the scope variables domains                
            -then we will remove pairs with matching domain assignment possibilites (eg (r,r) )
        """
        """psuedo code
            for each state in adj_dict.keys {
                constraint_dict.add(state)
                for each adj_state in adj_dict[state] {
                    scope <- (state, adj_state)
                    relation = CartesianProduct(domain_dict[state], domain_dict[adj_state])
                    for each r in relation {
                        if r.1 == r.2
                            relation.remove(r)
                    }
                }
            }
        """
        for state in self.adj_dict :
            self.constraints_dict[state] = []
            for adj_state in self.adj_dict[state] :
                scope = (state, adj_state)
                relation = list(product(self.domains_dict[state], self.domains_dict[adj_state]))
                for r in relation :
                    if r[0] == r[1] :
                        relation.remove(r)
                self.constraints_dict[state].append(relation)

        #print(self.constraints_dict["WA"])


    def getMRV(self) :
        """
            returns state(s) with minimum remaining in its domain
        """
        """pseudocode
            MRVstates = []
            MRV = inf
            for each state in domain_dict.keys {                                    for each states domain
                values = domain_dict[state].values.Count                            get its domain values
                if values < MRV and not colored_states_dict.contains(state) {       if # values less than MRV
                    MRV = values                                                    set MRV to that
                }
            }

            for each state in domain_dict.keys {                                                            iterate back through states
                if domain_dict[state].values.Count == MRV and not colored_states_dict.contains(state) {     anystate with same value as MRV
                    MRVstates.add(state)                                                                    gets added to MRV list
                }
            }

            return MRVstates


        """
        MRVstates = []
        mrv = math.inf
        for state in self.domains_dict :
            values = len(self.domains_dict[state])
            if values < mrv and not state in self.colored_states_dict :
                mrv = values
                print(mrv)
        for state in self.domains_dict :
            if len(self.domains_dict[state]) == mrv and not state in self.colored_states_dict :
                MRVstates.append(state)
        
        print(MRVstates)
        return MRVstates
    

            

    def getHighestDegree(self, states) :
        """
            returns state that hasn't been filled already that has most adjacent states
        """
        """pseudocode
            highestDegree = 0                                                   
            hdStates = []                                                      
            for each state in states {                                          for each state in subset provided
                adjacents = adj_dict[state].values
                if not colored_states_dict.keys.contains(state) {               if state is not already colored
                    currentAdjCount = 0                                         
                    for each adjstate in adjacents {                            for all that states adjacents 
                        if not colored_states_dict.keys.contains(adjstate) {    if they are not already colored 
                            currentAdjCount += adj_dict[state].values.Count     add #adjacents 
                        }
                    }
                    if currentAdjCount > highestDegree {                        after adding up degree, if higher than highest degree
                        highestDegree = currentAdjCount                         set highestDegree to adjacent count
                    }
                }
De
            }
            for each state in states {
                adjacents = adj_dict[state].values
                if adjacents.Count == highestDegree {
                    hdStates.add(state)
                }
            }
            return hdStates[]
        """
        pass

    def onePassState(self): 
        """pseudocode
        if iteration# is 0 and startState is not null {                 if we have a selected start state
            colored_states_dict.Add(startState, startColor)             then we color that first
        }
        else {                                                          otherwise we start with MCV
            nextState = null                                        
            MRVStates = getMRV()                                        get all states with the MRV
            if MRVStates.Count > 1 {                                    if more than one state has the same MRV 
                highestDegrees getHighestDegree(MRVStates)              get the highestDegree among them
                nextState = highestDegrees.random                       random will either choose the only one in there or a random highestDegree state
            }
            else {
                nextState = MRVStates[0]                                if one MRV, then use that
            }

            colorToSet = domain_dict[nextState].random
            colored_states_dict[nextState] = colorToSet      set to random color within domain
            
            for each state in adj_dict[nextState].values     remove color from all adjacent state domains
                domain_dict[state].remove(color)             

        }


        """
        pass

    def __init__(self, adj_dict, colors, startColor, startState) :
        self.adj_dict = adj_dict #this is X
        self.domains_dict = {} #this is D
        self.constraints_dict = {} #this is C
        #self.colors = colors
        self.colors = ["red","blue","green"]
        self.colored_states_dict = {}
        self.degree_dict = {}
        self.iterations = 0
        self.startState = startState
        self.startColor = startColor
        #print(f"Map colorer initialized with colors: {colors} and adj_dict: {adj_dict}")


        #init
        self.initializeDomains()
        self.initializeConstraints()
        self.getMRV()

  
