from flask import Flask
from routes import app as routes_blueprint
from models import initialize_db

app = Flask(__name__)

app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    initialize_db()

    app.run(debug=True)
