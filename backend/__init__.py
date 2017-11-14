from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__,
		static_folder = "../dist/static",
		template_folder = "../dist")

# cors, to setup that all endpoints are allowed to acces the 
# api end points.
cors = CORS(app, resources={r"/api/*": {"origings": "*"}})

from backend import views
from backend import api
