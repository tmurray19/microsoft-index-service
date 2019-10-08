from flask import render_template, request, Blueprint, url_for, jsonify
from flask_restplus import Api, Resource
from app import app
import logging, os



@app.route('/')
def index():
    return render_template('index.html')



api = Api(app)

@api.route('/chunk/<int:proj_id>')
class RenderChunk(Resource):
    def get(self, proj_id):
        pass


