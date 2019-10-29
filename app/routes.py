from flask import render_template, request, Blueprint, url_for, jsonify, send_file, send_from_directory
from flask_restplus import Api, Resource
from app import app
import logging, os
import uploader


@app.route('/captions/<int:proj_id>')
def show_index(proj_id):
    """
    Render catption vide editor
    """
    proj_id = str(proj_id)

    try:
        caption, vid, srt = uploader.get_insights(proj_id)
        return render_template('captions.html', proj_id=proj_id, player=vid, captions=caption, srt=srt)
    except:
        return render_template('error.html')
        
@app.route('/player/<string:proj_id>')
def show_player(proj_id):
    """
    Render catption vide editor
    """

    _caption, vid = uploader.get_insights(proj_id)
    return vid

@app.route('/download/captions/<string:proj_id>')
def download_captions(proj_id):
    captions = uploader.get_srt(proj_id)
    return send_file(captions)

api = Api(app)

@api.route('/initialise_upload/<string:proj_id>')
class InitialiseIndex(Resource):
    def get(self, proj_id):
        return uploader.create_queue_instance(proj_id)

@api.route('/index_upload/<string:proj_id>')
class UploadIndex(Resource):
    def get(self, proj_id):
        return uploader.upload_project_to_index(proj_id)

@api.route('/index_status/<string:proj_id>')
class GetIndex(Resource):
    def get(self, proj_id):
        return uploader.get_video_status(proj_id)


