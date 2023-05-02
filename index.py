
from flask import Flask, send_from_directory,render_template,request,redirect
from flask_restful import Api
import os
from flask_bootstrap import Bootstrap
import config
import model
import pandas as pd
import numpy as np
# import scanpy as sc
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
df_gene = pd.read_csv("/home/emmazhao/scTumorAtlas/fake_gene.csv")

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print(path)
    if path == "help":
        return send_from_directory(app.static_folder, path+'.html')
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/statistics',methods=['GET','POST'])
def statistics_page():
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
        if len(compare)==0: #get search result
            # search = model.DatabaseForm(request.form)
            cancer_type = search.data['cancer_type']
            # source = search.data['source']
            # metastasis = search.data['metastasis']
            # alteration_type = search.data['alteration_type']
            # tf = tf[tf['cancer_type'] == cancer_type]
            # tf = tf[tf['source'] == source]
            # tf = tf[tf['metastasis'] == metastasis]
            # tf = tf[tf['alteration_type'] == alteration_type]
            # tables = [tf_return[['checkbox','dataset_name','cancer_type','source','metastasis','alteration_type']]]
        else:
            first_graph = "frontend/graph/"+compare[0]+".png"
            second_graph = "frontend/graph/"+compare[1]+".png"
            return render_template('statistics.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            first_graph=first_graph, second_graph=second_graph, form=search)
    return render_template('statistics.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            form=search)


@app.route('/search_dataset',methods=['GET','POST'])
def search_dataset_page():
    search = model.DatabaseForm(request.form)
    pos_vals = np.zeros((len(df_gene),))
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(df_gene.index))),key=lambda x:x[0],reverse=True)]
    tf = df_gene.loc[idxs]
    index = list(range(len(tf)))
    tf_return = tf.loc[index]
    line_num = len(tf_return)
    tables = [tf_return[['dataset_name','cancer_type','source','metastasis','alteration_type','gene']]]
    if request.method == 'POST':
        gene = search.data['gene']
        cancer_type = search.data['cancer_type']
        source = search.data['source']
        metastasis = search.data['metastasis']
        if gene!="Any":
            tf = tf[tf['gene'] == gene]
        if cancer_type!="Any":
            tf = tf[tf['cancer_type'] == cancer_type]
        if source!="Any":
            tf = tf[tf['source'] == source]
        if metastasis!="Any":
            tf = tf[tf['metastasis'] == metastasis]
        tables = [tf[['dataset_name','cancer_type','source','metastasis','gene']]]
        print(line_num)
        return render_template('search_dataset.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            num=len(tables[0]), form=search)
    return render_template('search_dataset.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            num=line_num, form=search)

@app.route('/<cancer_type>')
def search_dataset_cancer_type(cancer_type):
    search = model.DatabaseForm(request.form)
    pos_vals = np.zeros((len(df_gene),))
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(df_gene.index))),key=lambda x:x[0],reverse=True)]
    tf = df_gene.loc[idxs]
    index = list(range(len(tf)))
    tf_return = tf.loc[index]
    line_num = len(tf_return)
    tables = [tf_return[['dataset_name','cancer_type','source','metastasis','gene']]]
    if cancer_type!="Any":
        tf = tf[tf['cancer_type'] == cancer_type]
    tables = [tf[['dataset_name','cancer_type','source','metastasis','gene']]]
    print(line_num)
    return render_template('search_dataset.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
        num=len(tables[0]), form=search)


@app.route('/dataset/<dataset_name>')
def dataset(dataset_name):
    dataset = df.loc["dataset_name"]

    cancer_type = dataset['cancer_type']
    source = dataset['source']
    metastasis = dataset['metastasis']
    alteration_type = dataset['alteration_type']
    cancer_type = dataset['cancer_type']

    cell_type_stat_img = "frondend/graph/"+dataset_name+".png"
    gene_table_file = "frondend/gene/"+dataset_name+".csv"
    gene_table = pd.read_csv(gene_table_file)
    
    index = list(range(len(gene_table)))
    tf_return = gene_table.loc[index]
    table = [tf_return[['dataset_name','cancer_type','source','metastasis','alteration_type','gene']]]

    return render_template('dataset.html',
                            dataset_name=dataset_name,
                            cancer_type=cancer_type,
                            source=source,
                            metastasis=metastasis,
                            alteration_type=alteration_type,
                            cell_type_stat_img=cell_type_stat_img,
                            table=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in table])


@app.route('/gene',methods=['GET','POST'])
def search_gene_page():
    gene_list = df_gene['gene']
    # input dataset should be a dataset with download address
    search = model.DatabaseForm(request.form)
    pos_vals = np.zeros((len(df_gene),))
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(df_gene.index))),key=lambda x:x[0],reverse=True)]
    tf = df_gene.loc[idxs]
    index = list(range(len(tf)))
    tf_return = tf.loc[index]
    tables = [tf_return[['checkbox','dataset_name','cancer_type','source','metastasis']]]
    if request.method == 'POST':
        gene = search.data['gene']
        cancer_type = search.data['cancer_type']
        source = search.data['source']
        metastasis = search.data['metastasis']
        tf = tf[tf['cancer_type'] == cancer_type]
        tf = tf[tf['source'] == source]
        tf = tf[tf['metastasis'] == metastasis]
        if gene not in gene_list:
            while True:
                gene = gene[:-1]
                if len(gene) == 0:
                    break
                t = [s for s in gene_list if gene in s]
                if len(t) > 0:
                    tf_return = tf_return[tf_return['gene'].isin(t)]
                    # gene = t.index[0]
                    break
        tables = [tf_return[['checkbox','dataset_name','cancer_type','source','metastasis']]]
        return render_template('gene.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            num=len(tables), form=search)
    return render_template('gene.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            num=79, form=search)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)