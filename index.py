
from flask import Flask, send_from_directory,render_template,request,redirect
from flask_restful import Api
import os
from flask_bootstrap import Bootstrap
import config
import model
import pandas as pd
import numpy as np
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
df = pd.read_csv("/home/emmazhao/scTumorAtlas/fake.csv")#.set_index("dataset_name")

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
    pos_vals = np.zeros((len(df),))
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(df.index))),key=lambda x:x[0],reverse=True)]
    tf = df.loc[idxs]
    index = list(range(len(tf)))#list(tf.columns)
    # tf.set_index('dataset_name')
    print(tf.index)
    tf_return = tf.loc[index]
    tables = [tf_return[['checkbox','dataset_name','cancer_type','source','metastasis','alteration_type']]]
    if request.method == 'POST':
        compare = request.form.getlist('first')
        print(request.form.getlist('first'))
        if len(compare==0): #get search result
            # search = model.DatabaseForm(request.form)
            cancer_type = search.data['cancer_type']
            print("cancer_type")
            # search = search.data['source']
            # metastasis = search.data['metastasis']
            # alteration_type = search.data['alteration_type']
            # tf = tf[tf['cancer_type'] == cancer_type]
            # tf = tf[tf['source'] == source]
            # tf = tf[tf['metastasis'] == metastasis]
            # tf = tf[tf['alteration_type'] == alteration_type]
            # tables = [tf_return[['checkbox','dataset_name','cancer_type','source','metastasis','alteration_type']]]
        else:
            first_graph = "frontend/graph/"+compare[0]+".jpg"
            second_graph = "frontend/graph/"+compare[1]+".jpg"
            return render_template('search.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            first_graph=first_graph, second_graph=second_graph, form=search)
    return render_template('search.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            form=search)

@app.route('/dataset/<dataset_name>')
def dataset(dataset_name):
    # if dataset_name not in df.index:
    #     dataset_name = dataset_name[:-1]
    #     if len(dataset_name) == 0:
    #         return redirect('/')
    #     t = df[df.index.str.contains(dataset_name)]
    #     if len(t) > 0:
    #         dataset_name = t.index[0]
    #         return redirect('/dataset/' + dataset_name)

    dataset = df.loc["dataset_name"]
    return render_template('dataset.html')


if __name__ == '__main__':
    app.run(threaded=True, port=5000)