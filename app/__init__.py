from flask import Flask

def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
