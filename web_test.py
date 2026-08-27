from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask works — 192-201"

if __name__ == "__main__":
    app.run()