from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from flasgger import Swagger


app = Flask(__name__)
app.config.from_object(Config)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Kinowave API",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

swagger = Swagger(app, template=swagger_template)

db = SQLAlchemy(app)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

