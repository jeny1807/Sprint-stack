from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/run-finaaal")
def run_finaaal():
    subprocess.run(["python", "finaaal.py"])
    return "✅ finaaal.py executed successfully!"

if __name__ == "__main__":
    app.run(debug=True)