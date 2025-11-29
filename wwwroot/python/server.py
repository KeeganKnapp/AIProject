from flask import Flask, request, jsonify
from flask_cors import CORS

import mapcoloring

global MapColorer

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
class ColoringRequest:
    def __init__(self, StateId: str, Index: int, Color: list[str]):
        self.StateId = StateId
        self.Index = Index
        self.Color = Color
        

@app.post("/api/start")
def start():
        data = request.get_json()

        coloring_request = ColoringRequest(
            StateId=data.get("StateId"),
            Index=data.get("Index"),
            Color=data.get("availableColors")
        )
        print("Got /api/start request:", data, flush=True)
        
        #init mapcolorer with colors and adj matrix
        adj_dict = load_adjacency_matrixes()
        colors = coloring_request.Color
        startColorIndex = coloring_request.Index
        startState = coloring_request.StateId
        init(adj_dict, colors, startState, startColorIndex)

        return jsonify({"status": "started"}), 200


def init(adj_dict, colors, startState, startColorIndex):
    MapColorer = mapcoloring.MapColorer(adj_dict, colors, startState, startColorIndex)


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
