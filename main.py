from flask import Flask
from database import testDatabaseConnection

if not testDatabaseConnection():
    exit()

app = Flask(__name__)

@app.route("/health")
def health():
    return "I'm up and running!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)