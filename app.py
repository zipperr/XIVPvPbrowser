# coding: utf-8
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Column, String, Text, ForeignKey, create_engine, MetaData, DECIMAL, DATETIME, exc, event, Index)
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.xivpvp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class GetData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(128), nullable=False)
    data = db.Column(db.Text, nullable=True)
    created = db.Column('created', DATETIME, default=datetime.now, nullable=False)

@app.route('/frontline/',methods = ['POST'])
def frontline():
    print(request.get_data().decode('utf-8'))
    newReq = GetData(contents='frontline', data=request.get_data().decode('utf-8'))
    db.session.add(newReq)
    db.session.commit()
    return "OKAY";

@app.route('/wolvesden/',methods =['POST'])
def wolvesden():
    print(request.get_data())
    newReq = GetData(contents=frontline, data=request.get_data().decode('utf-8'))
    db.session.add(newReq)
    db.session.commit()
    return "OKAY";

@app.route('/',methods = ['GET','POST'])
def home():
    allReq = GetData.query.all()
    return render_template('xivpvp.html', data=allReq)

@app.route('/<req>',methods = ['GET','POST'])
def req(req):
    print(request.method)
    print(request.url)
    print(request.headers)
    print(request.data)
    print(dict(request.args))

    newReq = GetData(contents=req, data=str(request.data))
    db.session.add(newReq)
    db.session.commit()
    allReq = GetData.query.all()
    return render_template('xivpvp.html', data=allReq)

@app.route('/del_data/<int:id>')
def del_data(id):
    del_data = GetData.query.filter_by(id=id).first()
    db.session.delete(del_data)
    db.session.commit()
    allReq = GetData.query.all()
    return render_template('xivpvp.html', data=allReq)

if __name__ == "__main__":
    # db.create_all()
    # app.run(debug=True, threaded=True, host="0.0.0.0", port=8080)
    app.run(debug=True, threaded=True, host="localhost", port=8000)
