from flask import Flask, Response
from sklearn.neighbors import KNeighborsClassifier
from flask import request
from sqlalchemy import *
from flask.ext.sqlalchemy import SQLAlchemy
import json
from flask import jsonify
from flask.ext.cors import CORS, cross_origin


#from sqlalchemy.sql import *

#from flaskext.mysql import MySQL
 
app = Flask(__name__)

cors = CORS(app, allow_headers='Content-Type')
app.config['CORS_HEADERS'] = 'Content-Type'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cityxplorer2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#Likes = db.Table('likes',
    
#)
class Likes(db.Model):
    id1 = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    place_id = db.Column(db.Integer)
    point = db.Column( db.Integer)
    longitude = db.Column( db.Float)
    latitude = db.Column(db.Float)
    type1 = db.Column(db.Integer)
class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column( db.Float)
    latitude = db.Column(db.Float)
    type = db.Column(db.Integer)
    name = db.Column(db.String)
    address = db.Column(db.String)

app.debug = True

@app.route("/", methods=['POST', 'GET'])
@cross_origin()

def hello():
	u_id = str(request.args.get('user_id'))
	print(u_id)
	likes = Likes.query.filter_by(user_id = u_id).all()
	places = Places.query.all()
	data = []
	train = []
	target = []
	visited = []
	find = []
	for i in range(len(likes)):
		ins = {}
		ins['id1'] = likes[i].id1
		ins['user_id'] = likes[i].user_id
		ins['place_id'] = likes[i].place_id
		ins['point'] = likes[i].point
		ins['longitude'] = likes[i].longitude
		ins['latitude'] = likes[i].latitude
		ins['type1'] = likes[i].type1
		ins1 = []
		ins1.append(likes[i].longitude)
		ins1.append(likes[i].latitude)
		ins1.append(likes[i].type1)

		visited.append(likes[i].place_id)
		
		train.append(ins1)
		target.append(likes[i].point)
		
		data.append(ins)
	#print(visited)
	plc = []
	place_names = {}
	for i in range(len(places)):
		if places[i].id not in visited:
			place_names[places[i].id] = places[i].name
			ins = []
			ins.append(places[i].longitude)
			ins.append(places[i].latitude)
			ins.append(places[i].type)
			find.append(ins)
			plc.append(places[i].id)
			#print(places[i].id)
	#print(train)
	#print(find)
	gnb = KNeighborsClassifier(n_neighbors=3)
	if len(find) > 0 and len(train) > 0:
		pred = gnb.fit(train, target).predict(find)
	else:
		pred = []
	#print(pred)
	a = []
	for i in range(len(pred)):
		b = [pred[i], plc[i]]
		a.append(b)
	#print(a)
	a.sort()
	ret = []
	for i in range(len(a) - 1, -1, -1):
		if len(ret) < 3:
			ret.append([a[i][1], place_names[a[i][1]]])
		else:
			break
		#print(i)
		#print(a[i][0])
	s = json.dumps(ret)
	print("Return" + s)
	resp = Response(response=s,
                    status=200,
                    mimetype="application/json")
	return resp

if __name__ == "__main__":
    app.run()