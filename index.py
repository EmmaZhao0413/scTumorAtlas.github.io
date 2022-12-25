
from flask import Flask, send_from_directory,render_template,request,redirect
from flask_restful import Api
import os
from flask_bootstrap import Bootstrap
import config
import model
# import controller

app = Flask(__name__, static_folder='frontend')#, instance_relative_config=True)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# MongoDB URI
# DB_URI = "mongodb+srv://Cansin:cv190499@a-star.roe6s.mongodb.net/A-Star?retryWrites=true&w=majority"
# app.config["MONGODB_HOST"] = DB_URI
bootstrap = Bootstrap(app)
config.init_app(app)
# config.init_db(app)
config.init_cors(app)

api = Api(app)

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(path)
    if path == "about":
        return send_from_directory(app.static_folder, path+'.html')
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/search',methods=['GET','POST'])
def search_page():
    # build search form by request
    search = model.DatabaseForm(request.form)
    # if request.method=='POST':
    #     return controller.search_database(search)
    return render_template('search.html',form=search)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)