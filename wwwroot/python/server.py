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
    def __init__(self, StateIds, SelectedColors, Colors):
        self.StateIds = StateIds
        self.SelectedColors = SelectedColors
        self.Colors = Colors

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
            Colors=data.get("Colors")
        )
        print("Got /api/start request:", data, flush=True)
        
        #init mapcolorer with colors and adj matrix
        adj_dict = load_adjacency_matrixes()
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
        domains_dict, stateId, color = MapColorer.onePassState()
        coloring_response = ColoringResponse(DomainsDict=domains_dict, StateId=stateId, Color=color)
        response_data = {
            "Domains": domains_dict,
            "StateId": coloring_response.StateId,
            "Color": coloring_response.Color
        }
        print("Responding with:", response_data, flush=True)
        return jsonify(response_data), 200




def load_adjacency_matrixes():
    state_adj_dict = {}
    with open("stateadjacency") as f:
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

        

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.run(host="127.0.0.1", port=5000, debug=True)
