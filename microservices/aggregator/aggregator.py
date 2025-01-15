from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)
client_weights = []

@app.route('/submit_weights', methods=['POST'])
def submit_weights():
    global client_weights
    try:
        weights = request.get_json()  # Correctly parses the JSON body.
        client_weights.append([np.array(w) for w in weights])  # Convert each weight to a NumPy array.
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 400


@app.route('/aggregate', methods=['GET'])
def aggregate_weights():
    global client_weights
    aggregated_weights = [np.mean([w[layer] for w in client_weights], axis=0) for layer in range(len(client_weights[0]))]
    client_weights = []  # Reset for the next round
    return jsonify([w.tolist() for w in aggregated_weights])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
