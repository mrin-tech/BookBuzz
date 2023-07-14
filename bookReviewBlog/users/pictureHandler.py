import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):

    filename = pic_upload.filename
    extentionType = filename.split('.')[-1]
    storageFilename = str(username) + '.' + extentionType

    filepath = os.path.join(current_app.root_path, 'static/profilePics', storageFilename)

    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storageFilename