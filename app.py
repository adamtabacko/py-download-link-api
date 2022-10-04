import sys
import socket

from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    version = sys.version_info
    return f"<p>Hello, World!</p></br>Running Python: {version.major}.{version.minor}.{version.micro}<br>Hostname: {socket.gethostname()}"
