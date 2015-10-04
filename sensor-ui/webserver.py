from flask import Flask, Response, render_template, flash, make_response
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from flask_wtf import Form, RecaptchaField
import sqlite3
import json
import csv
import StringIO
from flask import g

DATABASE = 'jonnyboards.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

app = create_app()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/data-json")
def all_data():
  q = """
      SELECT rowid, * FROM sensor_events ORDER BY rowid
      """
  cursor = get_db().cursor()
  cursor.execute(q)
  rows = cursor.fetchall()
  js = json.dumps(rows)
  resp = Response(js, status=200, mimetype='application/json')
  return resp

@app.route("/data-csv")
def all_csv_data():
  q = """
      SELECT rowid, * FROM sensor_events ORDER BY rowid
      """
  cursor = get_db().cursor()
  cursor.execute(q)
  rows = cursor.fetchall()
  si = StringIO.StringIO()
  cw = csv.writer(si)
  cw.writerows(rows)
  output = make_response(si.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=export.csv"
  output.headers["Content-type"] = "text/csv"
  return output



if __name__ == "__main__":
    app.run(debug=True)