from flask import Flask, request, jsonify
from src.http_interface import HttpInterface
import os
# from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
# GCP_PROJECT_ID = None
interface = HttpInterface(project="semiotic-effort-439102-k9")

# Route for handling GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Handle GET request
        data = request.get_json()
        if data:
            ret = interface.get(data)
            return jsonify(ret), 200
        else:
            return "Received a GET request!", 200
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            ret = interface.post(data)
            return jsonify(ret), 200
        else:
            return jsonify({"message": "Received a POST request with no data"}), 400

# Run the Flask app
if __name__ == '__main__':
    # load_dotenv()
    # GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    app.run(debug=True)
