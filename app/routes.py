from flask import render_template, request, Blueprint, url_for, jsonify, send_file, send_from_directory
from flask_restplus import Api, Resource
from app import app
import logging, os, json
import uploader


@app.route('/captions/<int:proj_id>')
def show_index(proj_id):
    """
    Render catption vide editor
    """
    proj_id = str(proj_id)

    try:
        caption, vid, _srt = uploader.get_insights(proj_id)
        vid_name = get_name(proj_id)
        return render_template('captions.html', proj_id=proj_id, player=vid, captions=caption, vid_name=vid_name)
    except:
        logging.exception('')
        return render_template('error.html')
        
# For refreshing captions
@app.route('/player/<string:proj_id>')
def show_player(proj_id):
    """
    Render catption vide editor
    """

    _caption, vid, _srt = uploader.get_insights(proj_id)
    return vid

@app.route('/download/captions/<string:proj_id>.srt')
def download_captions(proj_id):
    # This gets captions from indexer
    captions, _text = uploader.get_srt(proj_id)
    try:
        return send_file(captions, as_attachment=True, mimetype='text/srt', attachment_filename="{}_cc.srt".format(proj_id))
    except:
        logging.error("Error occurred during download_caption")
        logging.exception('')


api = Api(app)
# Creates JSON
@api.route('/initialise_upload/<string:proj_id>')
class InitialiseIndex(Resource):
    def get(self, proj_id):
        return uploader.create_queue_instance(proj_id)

# Uploads video to indexer service
@api.route('/index_upload/<string:proj_id>')
class UploadIndex(Resource):
    def get(self, proj_id):
        return uploader.upload_project_to_index(proj_id)

# Gets status of video
@api.route('/index_status/<string:proj_id>')
class GetIndex(Resource):
    def get(self, proj_id):
        return uploader.get_video_status(proj_id)

# Gets caption data
@api.route('/caption_data/<string:proj_id>')
class GetSRT(Resource):
    def get(self, proj_id):
        file_loc, _text = uploader.get_srt(proj_id)
        return file_loc


def get_name(proj_id):
    base_dir = os.path.join(app.config['BASE_DIR'], app.config['VIDS_LOCATION'], str(proj_id))
    file_location = os.path.join(base_dir, 'FinalSubclipJson.json')

    json_data = json.load(open(file_location, 'r'))

    return json_data['Name']
    
