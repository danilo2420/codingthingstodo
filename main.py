from flask import Flask
from database import testDatabaseConnection
from blueprints.ideas import ideas_bp

if not testDatabaseConnection():
    exit()

app = Flask(__name__)

@app.route("/health")
def health():
    return "I'm up and running!"

app.register_blueprint(ideas_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)