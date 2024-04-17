from flask import Flask
from flask_smorest import Api
from services.question_service import blp as question_blp
from services.subject_service import blp as subject_blp
from services.user_service import blp as user_blp

app = Flask(__name__)
app.config["API_TITLE"] = "QuestionsAPI"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "apidocs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.52.0"
app.config["OPENAPI_REDOC_PATH"] = "redoc"
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
api = Api(app)
api.register_blueprint(user_blp)
api.register_blueprint(subject_blp)
api.register_blueprint(question_blp)


if __name__ == '__main__':
    app.run()


