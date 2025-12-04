from flask import Flask, request, jsonify
from flask_cors import CORS
import mapcoloring

MapColorer = None

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def init(adj_dict, colors, startStates, startColors):
    global MapColorer
    MapColorer = mapcoloring.MapColorer(adj_dict, colors, startStates, startColors)

class ColoringRequest:
    def __init__(self, StateIds, SelectedColors, Colors, Map):
        self.StateIds = StateIds
        self.SelectedColors = SelectedColors
        self.Colors = Colors
        self.Map = Map

class ColoringResponse:
    def __init__(self, DomainsDict, StateId, Color):
        self.DomainsDict = DomainsDict
        self.StateId = StateId
        self.Color = Color


@app.post("/api/start")
def start():
        data = request.get_json()

        coloring_request = ColoringRequest(
            StateIds=data.get("StateIds"),
            SelectedColors=data.get("SelectedColors"),
            Colors=data.get("Colors"),
            Map=data.get("Map")
        )
        print("Got /api/start request:", data, flush=True)
        
        #init mapcolorer with colors and adj matrix
        if(coloring_request.Map == "us-map") :
            adj_dict = load_adjacency_matrixes()
        elif(coloring_request.Map == "ohio-map") :
            adj_dict = load_ohio_adjacency_matrixes()
        else :
            adj_dict = {}
        print("Initialized adjacency dict")
        
        init(adj_dict, coloring_request.Colors, coloring_request.StateIds, coloring_request.SelectedColors)
        print("Initialized mapcolorer")

        states = []
        for state in adj_dict.keys():
            states.append(state)
        
        return jsonify(states), 200


@app.get("/api/runonce")
def run_once():
        print("Got /api/runonce request", flush=True)
        if MapColorer is None:
            print("MapColorer not initialized, post start first")
        used_colors, colored_states_dict, domains_dict, state_id, color = MapColorer.onePassState()
        response_data = {
            "Domains": domains_dict,
            "StateId": state_id,
            "Color": color,
            "ColoredStates": colored_states_dict, 
            "UsedColors": used_colors
        }
        print("Responding with:", response_data, flush=True)
        return jsonify(response_data), 200




def load_adjacency_matrixes():
    state_adj_dict = {}
    with open("usaadjacency") as f:
        for line in f:
            state = line[0:2]
            state_adj_dict[state] = []
            for c in range(3, len(line), 3) :
                adjancent = line[c:c+2]
                state_adj_dict[state].append(adjancent)
                
    """ test dicts
    for key, value in state_adj_dict.items() :
        print(key, end=": ")
        print(value)
    """

    return state_adj_dict

def load_ohio_adjacency_matrixes():
    county_adj_dict = {}
    with open("ohioadjacency") as f:
        for line in f:
            county = line[:line.index(" County")]
            if county not in county_adj_dict:
                county_adj_dict[county] = []
            secondBarIndex = line.find('|', line.index('|') + 1)
            commaIndex = line.find(',', secondBarIndex)
            if "OH" not in line[commaIndex::] :
                continue
            adjCounty = line[secondBarIndex + 1:commaIndex]
            adjCounty = adjCounty[0:adjCounty.find(" County")]
            county_adj_dict[county].append(adjCounty)

    print(county_adj_dict)
    return county_adj_dict
        

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    app.run(host="127.0.0.1", port=5000, debug=True)
