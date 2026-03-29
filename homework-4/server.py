from flask import Flask, jsonify, request, Response
from dotenv import dotenv_values
from controllers import operation

app = Flask(__name__)


@app.route("/")
def server_info() -> str:
    return "My server"

@app.route("/author")
def author() -> Response:
    author = {
        "name": "Artem",
        "course": 2,
        "age": 19,
    }
    return jsonify(author)

@app.route("/sum")
def runner() -> Response:
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    return jsonify({'sum': operation(a, b)})

def get_port() -> int:
    config = dotenv_values(".env")
    if "PORT" in config:
        return int(config["PORT"])
    return 5000

if __name__ == "__main__":
    app.run(debug=True, port=get_port())

