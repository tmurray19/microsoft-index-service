from flask import render_template, request, Blueprint, url_for, jsonify
from flask_restplus import Api, Resource
from app import app
import logging, os
import uploader


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/captions/<string:proj_id>')
def show_index(proj_id):
    """
    Render catption vide editor
    """

    caption, vid = uploader.get_insights(proj_id)
    return render_template('captions.html', proj_id=proj_id, player=vid, captions=caption)

@app.route('/player/<string:proj_id>')
def show_player(proj_id):
    """
    Render catption vide editor
    """

    _caption, vid = uploader.get_insights(proj_id)
    return vid


api = Api(app)

@api.route('/chunk/<int:proj_id>')
class RenderChunk(Resource):
    def get(self, proj_id):
        pass


