import os
from flask import render_template, request, redirect, jsonify, current_app
from werkzeug.utils import secure_filename
from . import web

from app.utils.html_parser import html_to_rich_text
from app.utils.get_file_extension import getFileExtension

@web.route("/")
def index():
    return render_template("index.html")

@web.route("/send-message", methods=["POST"])
def queue_message():
    try:
        data = request.get_json()
        message = data['message']
        parsed = html_to_rich_text(message)
        current_app.queue.put(parsed)
        return jsonify({"success": True, "message": "Message added to the queue"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@web.route("/send-image", methods=["POST"])
def queue_image():
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and (getFileExtension(file.filename) in ["jpg", "jpeg", "png"]):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        current_app.queue.put(filepath)
        return redirect("/")
    else:
        return "Invalid file type"