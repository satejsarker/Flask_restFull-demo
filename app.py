
from flask import Flask,jsonify,request
from flask_restful import Resource, Api, reqparse, fields, marshal_with,abort
from flask_sqlalchemy import  SQLAlchemy
from bson import json_util

import  json
from pymongo import  MongoClient,errors
app = Flask(__name__)
api=Api(app)
app.config['Debug']=True
try:
    clint=MongoClient('mongodb://localhost:4100/')
    Mdata=clint.info
    Information=Mdata.info
    print 'database connected'
except errors.ConnectionFailure, e:
    print('database connection error %s',e)
#data type in info
atrInfo={}
atrInfo['name']=fields.String
atrInfo['age']=fields.Integer
atrInfo['des']=fields.String

parser = reqparse.RequestParser()
parser.add_argument('Info',location='json')


resource_fields = {
    'info':fields.Nested(atrInfo),
'uri':    fields.Url('informationhub')
}

# app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://satej:satej@localhost:3306/flask'
# db=SQLAlchemy(app)
#
# class History(db.Model):
#     __tablename__='history'
#     id=db.Column('id',db.Integer,primary_key=True)
#     job=db.Column('job',db.String(100))
#     salary=db.Column('salary',db.Integer)



class HelloWorld(Resource):
    def get(self):

        return {'hello':'world'}


    def post(self):
        args=parser.parse_args()
        jData=request.get_json(force=True)["Info"]
        dataINput=Information.insert_one(jData)

        return jsonify(data={'status':"ok"})
        # return args['Info']
class InformationHub(Resource):
    @marshal_with(resource_fields,envelope='Information')
    def get(self,**kwargs):
        info1 =Mdata.info
        try:
            result = info1.find({})
            data = []

            for res in result:
                
                print res
                data.append(res)
            if (len(data)==0):
                abort(204, message="Data {} doesn't exist".format('not  Found'))
            return {'info': sorted(data,key=lambda k: k['name'])}, 200, {'Etag': 'Request success '}
        except:
            abort(400, message="Data {} ".format('not  Found'))
            return


        # abort(404, message="Data {} doesn't exist".format(data))


api.add_resource(HelloWorld,'/')
api.add_resource(InformationHub,'/info')

# @app.route('/')
# def hello_world():
#     return 'Hello World!'

@app.route('/rest1',methods=['GET'])
def rest_get():
    # val = History.qurry.all()
    return  jsonify({
        'topic':'get request',
        'api':'API_version:1.0.1',
        "data":{}
    })
if __name__ == '__main__':
    app.run( debug=True, port=8080)
