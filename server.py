import os
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    # Optionally call your script here
    return "App is running!"

@app.route("/run")
def run_script():
    result = subprocess.run(["./frame.sh"], capture_output=True, text=True)
    return f"<pre>{result.stdout}\n{result.stderr}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
