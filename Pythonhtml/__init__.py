from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:password@localhost/Hotel"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = "waikiki"
app.config["SECRET_KEY"] = '43fed32314d207a75d518814a4c5cab7'
db = SQLAlchemy(app)
login_manager= LoginManager(app)
login_manager.login_view = "loggain"
login_manager.login_message_category = "failure"
login_manager.login_message = "Du måste logga in för att boka rum"
from Pythonhtml import routes
