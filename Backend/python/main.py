from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
#Esta linea permite a la api hacer peticiones externas o desde otrso programas
cors = CORS(app, resources={r"/*": {"origin": "*"}})

@app.route("/", methods=['GET'])
def hello_world():
    recibido = request.json["user"]
    otro = request.json["pass"]
    print(recibido)
    return jsonify({"user": "bien"})
if __name__ == "__main__":
    app.run(debug=True, port=5000)

