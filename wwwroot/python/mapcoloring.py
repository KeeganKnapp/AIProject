from itertools import product 
import math
import random
import copy

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
                self.constraints_dict[state].append((scope, relation))


        print("initialized constraints...")


    def getMRV(self, exclude = []) :
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
            if state in exclude :   #this is for attempting to find next lowest mrv to keep coloring going if trapped
                continue 
            values = len(self.domains_dict[state])
            if values < mrv and not state in self.colored_states_dict :
                mrv = values
                print(mrv, end=" ")
                print(state, end = " ")
        for state in self.domains_dict :
            if state not in exclude and len(self.domains_dict[state]) == mrv and not state in self.colored_states_dict :
                MRVstates.append(state)
        
        print(f"MRV {MRVstates}")
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
        highestDegree = 0
        hdState = None
        for state in states :

            print(f"finding adjacent state count for {state}")
            adj_count = 0
            for adjState in self.adj_dict[state] :
                if adjState not in self.colored_states_dict :
                    print(f"{adjState} not colored yet, adding to count")
                    adj_count += 1
            if adj_count >= highestDegree :
                highestDegree = adj_count
                hdState = state

        print(f"Highest degree: {highestDegree}")
        
        return hdState


    def checkValidity(self, state, color) :
        """
            check whether assignment fits constraint for all state relations
        """
        """pseudocode
        bool valid = false
        for adjState in adj_dict[state] {                                                   for every adjacent state to the state we want to color     
            if adjState in colored_states_dict {                                            if the state is colored already 
                adjColor = colored_states_dict[adjState]                                    store the color of that adjacent state
                for c in constraints_dict[state] {                                          for each of our requested states constraints 
                    if(c[0][1] == adjState) {                                               find the constraint for the current adjacent state
                        for relation in c[1]                                                for every relation in that constraint
                            if relation.contains(color) and relation.contains(adjColor)     if the relation contains our color and the adj state color
                                valid = true                                                is valid
                    }
                }
            }
        }
        """

        #get all colored states
        adjColoredStates = {}
        for adjState in self.adj_dict[state] :                                                  
            if adjState in self.colored_states_dict :
                adjColoredStates[adjState] = self.colored_states_dict[adjState]

        print(f"{state} colored adjacents: {adjColoredStates}")

        #return true if no colored adjacent states
        if len(adjColoredStates) == 0 :
            print(f"{state} has no colored adjacents")
            return True

        #if any arent in scope of constraints
        for coloredAdj in adjColoredStates :
            in_scope = False     
            for constraint in self.constraints_dict[state] :
                if coloredAdj in constraint[0] :
                    in_scope = True
            if in_scope :
                pass
            else :
                print(f"{coloredAdj} not in scope of {state}")
                return False

        #check if relation contains color, adjColor
        for coloredAdj in adjColoredStates :
            for constraint in self.constraints_dict[state] :
                if coloredAdj in constraint[0] :
                    contains_relation = False
                    for relation in constraint[1] :
                        if relation[0] == color and relation[1] == self.colored_states_dict[coloredAdj] :
                            print(f"relation ({color},{self.colored_states_dict[coloredAdj]}) IS in relations {constraint[1]} ")
                            return True
                    print(f"relation ({color},{self.colored_states_dict[coloredAdj]}) is NOT in relations {constraint[1]} ")
                    return False

    def updateDomains(self, state, color) :
        for adjState in self.adj_dict[state] :
            #if adjState not in self.colored_states_dict :
            if color in self.domains_dict[adjState] :
                self.domains_dict[adjState].remove(color)
            


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

        self.iterations += 1
        nextState = None
        colorToSet = None

        excludedStates = []
        attempts = 0
        while attempts < 6 and (nextState is None or len(self.domains_dict[nextState]) == 0) :
            MRVStates = self.getMRV(excludedStates)
            if len(MRVStates) > 1 :
                highestDegree = self.getHighestDegree(MRVStates)  #if multiple mrv use highest degree
                nextState = highestDegree

            elif len(MRVStates) == 1 :
                nextState = MRVStates[0]                          #if one mrv use that

            if len(self.domains_dict[nextState]) == 0 :
                excludedStates.append(nextState)
            attempts += 1


        #get random color in domain and not already used
        if self.domains_dict[nextState] != [] :
            if not nextState in self.used_colors:
                self.used_colors[nextState] = []

            #while colorToSet is None or colorToSet in self.used_colors[nextState] :
            #colorToSet = rndom.choice(self.domains_dict[nextState])
            availableColors = list(set(self.domains_dict[nextState]).difference(set(self.used_colors[nextState])))

            if len(availableColors) > 0 :
                print(f"available colors for {nextState} : {availableColors}")
                colorToSet = random.choice(availableColors)

        if (nextState is not None 
           and colorToSet is not None
           and len(self.domains_dict[nextState]) > 0
           and self.checkValidity(nextState,colorToSet)) :

            #save domains to stack
            self.domains_stack.append(copy.deepcopy(dict(self.domains_dict)))

            #color state
            self.colored_states_dict[nextState] = colorToSet
            self.updateDomains(nextState,colorToSet)

            #add to state fringe and colors used
            self.fringe.append(nextState)
            self.used_colors[nextState].append(colorToSet)

            
            print("successful CSP run")
        else :
            print("cannot color state, attempting backtrack")
            self.used_colors[nextState] = []
            nextState, colorToSet = self.backTrack()

        return self.used_colors, self.colored_states_dict, self.domains_dict, nextState, colorToSet
            
    def backTrack(self) :
        """
        track all domains at each step in forward stepping function so we can backtrack later
        also track each state and its used colors so far
        when we hit a wall at a state, pop the last domains set and set to current
        then pop the last state and select a new color from list of available colors left
        when a popped states options are exhausted, pop the next state and reset to that domain

        """
        self.domains_dict = self.domains_stack.pop()    #set current domains to last domains saved
        lastState = self.fringe.pop()                #get last state colored
        self.colored_states_dict.pop(lastState)         #de-color state
        return lastState, "#ffffff"                     #set state white

    def __init__(self, adj_dict, colors, startStates, startColors) :
        self.adj_dict = adj_dict #this is X
        self.domains_dict = {} #this is D
        self.constraints_dict = {} #this is C,  ["WA"][ { (WA, ID), ('red','green')
        self.colors = colors
        self.colored_states_dict = {}
        self.iterations = 0
        self.fringe = []    #stack of colored states
        self.domains_stack = []
        self.used_colors = {}

        #init
        self.initializeDomains()
        self.initializeConstraints()

        #add start state + color if set
        if startStates != [] :
            for i, state in enumerate(startStates) :
                color = colors[startColors[i]]
                print(f"Removing {color} from {state} adjacent states domains")
                self.colored_states_dict[state] = color
                self.updateDomains(state, color)
        
  
