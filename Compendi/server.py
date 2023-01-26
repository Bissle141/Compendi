from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db
from jinja2 import StrictUndefined
import os
import crud
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary

# App & Secret Key config
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

#  Cloudinary Config
cloudinary.config(
  cloud_name = os.environ['CLOUDNAME'],
  api_key = os.environ['CLOUDAPIKEY'],
  api_secret = os.environ['APISECRET'],
  secure = True
)

# Upload
upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id="olympic_flag")
# Transform
url, options = cloudinary_url("olympic_flag", width=100, height=150, crop="fill")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)