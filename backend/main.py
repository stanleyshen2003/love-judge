from flask import Flask, request, jsonify
from src.http_interface import HttpInterface
import os
from flask_cors import CORS
# from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# GCP_PROJECT_ID = None
interface = HttpInterface(project="semiotic-effort-439102-k9")

# Route for handling GET and POST requests
@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    if data:
        ret = interface.post(data)
        return jsonify(ret), 200
    else:
        return jsonify({"message": "Received a POST request with no data"}), 400
    
@app.route('/', methods=['GET'])
def get():
    user = request.args.get('user')
    ret = interface.get({'sender': user})
    return jsonify(ret), 200

@app.route('/lawyer', methods=['POST'])
def index():
    data = request.get_json()
    if data:
        ret = interface.post_lawyer(data)
        return jsonify(ret), 200
    else:
        return jsonify({"message": "Received a POST request with no data"}), 400
    
@app.route('/lawyer', methods=['GET'])
def get():
    user = request.args.get('user')
    ret = interface.get_lawyer(user)
    return jsonify(ret), 200


# Run the Flask app
if __name__ == '__main__':
    # load_dotenv()
    # GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    app.run(debug=True, host='0.0.0.0')
