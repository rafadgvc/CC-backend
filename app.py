import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from services.user_service import blp as user_blp
from services.exam_service import blp as exam_blp
from services.question_service import blp as question_blp
from services.subject_service import blp as subject_blp
from services.node_service import blp as node_blp
from services.result_service import blp as result_blp
from secret import JWT_SECRET_KEY

app = Flask(__name__)
app.config["API_TITLE"] = "QuestionsAPI"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "apidocs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.52.0"
app.config["OPENAPI_REDOC_PATH"] = "redoc"
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


api = Api(app)
api.register_blueprint(user_blp)
api.register_blueprint(subject_blp)
api.register_blueprint(node_blp)
api.register_blueprint(question_blp)
api.register_blueprint(exam_blp)
api.register_blueprint(result_blp)


if __name__ == '__main__':
    app.run()


