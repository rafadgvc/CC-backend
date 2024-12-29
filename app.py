import os
from datetime import timedelta
import logging

from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from services.user_service import blp as user_blp
from services.exam_service import blp as exam_blp
from services.question_service import blp as question_blp
from services.subject_service import blp as subject_blp
from services.node_service import blp as node_blp
from services.result_service import blp as result_blp
from secret import JWT_SECRET_KEY

logging.basicConfig(
    filename='api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config["API_TITLE"] = "StratExam"
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
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///:memory:")
if os.getenv('FLASK_ENV') == 'testing':
    app.config["TESTING"] = True
    app.config["DEBUG"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///:memory:")
jwt = JWTManager(app)



@app.before_request
def log_request_info():
    logging.info(f"Petición {request.method} en {request.path} desde {request.remote_addr}")

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
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
    app.run(host="0.0.0.0", port=5000)


