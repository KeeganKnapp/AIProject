from flask import Flask, request, jsonify
from flask_cors import CORS
import mapcoloring

MapColorer = None

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


class ColoringRequest:
    def __init__(self, StateId: str, Index: int, Color: list[str]):
        self.StateId = StateId
        self.Index = Index
        self.Color = Color

class ColoringResponse:
    def __init__(self, StateId: str, Color: str):
        self.StateId = StateId
        self.Color = Color

def init(adj_dict, colors, startState, startColorIndex):
    global MapColorer
    MapColorer = mapcoloring.MapColorer(adj_dict, colors, startState, startColorIndex)

@app.post("/api/start")
def start():
        data = request.get_json()

        coloring_request = ColoringRequest(
            StateId=data.get("stateId"),
            Index=data.get("colorIndex"),
            Color=data.get("availableColors")
        )
        print("Got /api/start request:", data, flush=True)
        
        #init mapcolorer with colors and adj matrix
        adj_dict = load_adjacency_matrixes()
        colors = coloring_request.Color
        startColorIndex = coloring_request.Index
        startState = coloring_request.StateId
        print(f"Starting with starting state: {startState}, starting color {colors[startColorIndex]}")
        init(adj_dict, colors, startState, colors[startColorIndex])

        return jsonify({"status": "started"}), 200



@app.get("/api/runonce")
def run_once():
        print("Got /api/runonce request", flush=True)
        if MapColorer is None:
            print("MapColorer not initialized, post start first")
        stateId, color = MapColorer.onePassState()
        coloring_response = ColoringResponse(StateId=stateId, Color=color)
        response_data = {
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
