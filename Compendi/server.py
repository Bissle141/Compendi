from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db
from jinja2 import StrictUndefined
import os
import crud

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']