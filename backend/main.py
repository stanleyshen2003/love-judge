from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Route for handling GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Handle GET request
        return "Received a GET request!", 200
    elif request.method == 'POST':
        # Handle POST request
        data = request.get_json()  # Get the JSON data sent in the request
        if data:
            return jsonify({"message": "Received a POST request", "data": data}), 200
        else:
            return jsonify({"message": "Received a POST request with no data"}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
