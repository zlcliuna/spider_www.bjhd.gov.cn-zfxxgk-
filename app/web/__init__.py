from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import search
from app.web import index