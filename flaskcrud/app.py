#from typing_extensions import Required
from flask import Flask, request,render_template,url_for
from flask_restful import Resource, Api,reqparse,abort,marshal_with,fields
from flask_mongoengine import MongoEngine
from werkzeug.utils import redirect
from flask_cors import CORS



app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'db':'usersdatabaseflask',
    'host':'localhost',
    'port':27017
}

db = MongoEngine()
db.init_app(app)

class UserModel(db.Document):
   
    name = db.StringField(max_length = 50)
    email = db.StringField(max_length=50)
    password = db.StringField(max_length=50)


user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name",type = str,help = "name is required",required = True)
user_post_args.add_argument("email",type = str,help = "email is required",required = True)
user_post_args.add_argument("password",type = str,help = "password is required",required = True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name",type = str,help = "name is required",required = True)
user_put_args.add_argument("email",type = str,help = "email is required",required = True)
user_put_args.add_argument("password",type = str,help = "password is required",required = True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name",type = str,help = "name is required")
user_update_args.add_argument("email",type = str,help = "email is required")
user_update_args.add_argument("password",type = str,help = "password is required")

user_login_post_args = reqparse.RequestParser()
user_login_post_args.add_argument("email",type = str,help = "email is required",required = True)
user_login_post_args.add_argument("password",type = str,help = "password is required",required = True)

resource_fields = {
    
    'name':fields.String,
    'email':fields.String,
    'password':fields.String

}

class Register(Resource):
    @marshal_with(resource_fields)
    def get(self,userid):
        user=UserModel.objects.get(_id = userid)
        if not user:
            abort(404,message = "could not find the user with that id")
        return user
    
    @marshal_with(resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        print("args is",args['name'])
        res=UserModel.objects.filter(email = args['email']).first()
        if res:
            abort(409,message = "User already exists..")
            
        #result = UserModel.query.filter_by(_id = userid).first()
        #if result:
         #   abort(404,message = "user already present")
        user = UserModel(name = args['name'],email = args['email'],password = args['password']).save()
        return user,201

    
    @marshal_with(resource_fields)
    def put(self,userid):
        args = user_update_args.parse_args()
        if args['name']:
            UserModel.objects.get(_id = userid).update(name = args['name'])
        if args['email']:
            UserModel.objects.get(_id = userid).update(email = args['email'])
        if args['password']:
            UserModel.objects.get(_id = userid).update(email = args['password'])
        return "{} updated".format(userid),200

    def delete(self,userid):
        UserModel.objects.get(_id = userid).delete()
        return "User deleted",204



class Login(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = user_login_post_args.parse_args()
        
        print("login args is ",args['email'])
        res=UserModel.objects.filter(email = args['email']).first()
        if not res:
            abort(400,message = "bad request user not found")

        if(res.email == args['email'] and res.password == args['password']):
            print("yes")
            return res,200



api.add_resource(Register, '/adduser/<int:userid>','/adduser')
api.add_resource(Login, '/loginuser')






@app.route("/")
def landingpage():
    return "<h1>landing page</h1>"


if __name__ == '__main__':
    app.run(debug=True)