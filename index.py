
from flask import Flask, send_from_directory,render_template,request,redirect
from flask_restful import Api
import os,csv
from flask_bootstrap import Bootstrap
import config
import model
import pandas as pd
import numpy as np
# import scanpy as sc

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
df = pd.read_csv("/home/emmazhao/scTumorAtlas/data/fake.csv")#.set_index("dataset_name")
dataset_info = pd.read_csv("/home/emmazhao/scTumorAtlas/data/general_table_for_all_datasets_with_reference_new_for_Emma_0527.csv")
fusion_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/used_general_fusion_info_0529.csv')
gene_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/gencode_v19_gene_info.csv')

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
    tables = [tf_return[['checkbox','dataset_name','cancer_type','source','metastasis']]]
    if request.method == 'POST':
        compare = request.form.getlist('first')
        print(request.form.getlist('first'))
        if len(compare)==0: #get search result
            cancer_type = search.data['cancer_type']
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
    pos_vals = np.zeros((len(dataset_info),))
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(dataset_info.index))),key=lambda x:x[0],reverse=True)]
    tf = dataset_info.loc[idxs]
    index = list(range(len(tf)))
    tf_return = tf.loc[index]
    line_num = len(tf_return)
    tables = [tf_return[['dataset_name','cancer_type','source','metastasis','alteration_type','gene']]]
    total_num = len(dataset_info.index)
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
            num=len(tables[0]), form=search, total_num=total_num)
    return render_template('search_dataset.html',table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in tables],
            num=line_num, form=search)

@app.route('/search_dataset/<cancer_type>')
def search_dataset_cancer_type(cancer_type):
    search = model.DatabaseForm(request.form)
    pos_vals = np.zeros((len(dataset_info),))
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(dataset_info.index))),key=lambda x:x[0],reverse=True)]
    tf = dataset_info.loc[idxs]
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
    # dataset_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/general_table_for_all_datasets_with_reference_new_for_Emma_0527.csv')
    dataset_info = dataset_info.T
    dataset_info.columns = dataset_info.iloc[0]
    dataset_info["info_type"] = dataset_info.index
    summary = dataset_info.loc[["Cancer type","#Cells"]]
    cancer_type = dataset_info.loc["Cancer type"][dataset_name]
    num_cell = dataset_info.loc["#Cells"][dataset_name]
    experiments = dataset_info.loc[["#Conditions/Donors","Conditions/Donors colnames","Conditions/Donors names"]]
    cell_types = dataset_info.loc[["#Melanocyte","#Hepatocyte","#Epithelial cell","#Fibroblast","#Endothelial cell",
                                   "#B/Plasma cell","#T/NK cell","#Macro/Mono/DC","#Oligodendrocyte","#Neuron",
                                   "#Astrocyte","#HSC","#Malignant cell"]]
    publication = dataset_info.loc[["Reference title","Publish time","doi","GSEid"]]
    sample = dataset_info.loc[["source","tumor_abbreviation","tumor_name","metastatic_or_primary"]]
    summary = [summary[[dataset_name]]]
    experiments = [experiments[["info_type",dataset_name]]]
    cell_types = [cell_types[["info_type",dataset_name]]]
    publication = [publication[["info_type",dataset_name]]]
    sample = [sample[["info_type",dataset_name]]]
    plot ="../frontend/graph/plot2.png"
    return render_template('dataset.html',
                           plot=plot,
                            dataset_name=dataset_name,
                            cancer_type=cancer_type,
                            num_cell=num_cell,
                            table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in experiments],
                            table2=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in cell_types],
                            table3=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in publication],
                            table4=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in sample])


@app.route('/fusion/<fusion_name>')
def fusion(fusion_name):
    dataset_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/used_general_fusion_info_0529.csv')
    fusion_gene_1 = fusion_name.strip().split("_")[0]
    fusion_gene_2 = fusion_name.strip().split("_")[1]
    row = dataset_info.loc[(dataset_info['fusion_gene_1'] == fusion_gene_1) & (dataset_info['fusion_gene_2'] == fusion_gene_2)]
    print(row["#FusionName"].values.item())
    # FusionName = row["#FusionName"].values.item()
    Position_from = row["#FusionName_and_pos"].values.item().strip().split(";")[1]
    Position_to = row["#FusionName_and_pos"].values.item().strip().split(";")[2]
    SpliceType = row["SpliceType"].values.item()
    LeftBreakDinuc = row["LeftBreakDinuc"].values.item()
    RightBreakDinuc = row["RightBreakDinuc"].values.item()
    plot ="../frontend/graph/plot1.png"

    LeftGene = row["LeftGene"].values.item().strip().split("^")[1]
    RightGene = row["RightGene"].values.item().strip().split("^")[1]
    gene_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/gencode_v19_gene_info.csv')
    row = gene_info.loc[((gene_info['gene_id'] == LeftGene) | (gene_info['gene_id'] == RightGene))]
    row = [row[['gene_link','chromosome','start','end','strand','gene_name','exon_length']]]
    return render_template('fusion.html',
                            fusion_name=fusion_name,
                            Position_from=Position_from,
                            Position_to=Position_to,
                            SpliceType=SpliceType,
                            LeftBreakDinuc=LeftBreakDinuc,
                            RightBreakDinuc=RightBreakDinuc,
                            plot=plot,
                            table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in row])


@app.route('/gene/<gene_id>')
def gene(gene_id):
    dataset_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/gencode_v19_gene_info.csv')
    row = dataset_info.loc[dataset_info['gene_id'] == gene_id]
    gene_name = row["gene_name"].values.item()
    chromosome = row["chromosome"].values.item()
    start = row["start"].values.item()
    end = row["end"].values.item()
    strand = row["strand"].values.item()
    exon_length = row["exon_length"].values.item()
    print(gene_name)

    fusion_info = pd.read_csv('/home/emmazhao/scTumorAtlas/data/used_general_fusion_info_0529.csv')
    row = fusion_info.loc[((fusion_info['fusion_gene_1'] == gene_name) | (fusion_info['fusion_gene_2'] == gene_name))]
    print(row)
    row = [row[['#FusionName','SpliceType','LeftGene','RightGene']]]
    # row = list(row["#FusionName"].values)
    plot1 ="../frontend/graph/plot3.png"
    return render_template('gene.html',
                           gene_name=gene_name,
                            gene_id=gene_id,
                            chromosome=chromosome,
                            start=start,
                            end=end,
                            strand=strand,
                            exon_length=exon_length,
                            plot1=plot1,
                            table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in row])

@app.route('/search_gene',methods=['GET','POST'])
def search_gene_page():
    # input dataset should be a dataset with download address
    search = model.DatabaseForm(request.form)
    if request.method == 'POST':
        gene_name = search.data['gene']
        fusion_name = search.data['fusion']
        if len(gene_name)>0:
            row = gene_info.loc[gene_info['gene_name'] == gene_name]
            row = [row[['gene_id','gene_link','chromosome','start','end','strand','gene_name','exon_length']]]
            return render_template('search_gene.html',form=search,
                            table1=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in row])
        elif len(fusion_name)>0:
            fusion_gene_1 = fusion_name.strip().split("_")[0]
            fusion_gene_2 = fusion_name.strip().split("_")[1]
            row = fusion_info.loc[(fusion_info['fusion_gene_1'] == fusion_gene_1) & (fusion_info['fusion_gene_2'] == fusion_gene_2)]
            row = [row[['#FusionName','SpliceType','LeftGene','RightGene']]]
            return render_template('search_gene.html',form=search,
                            table2=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in row])
        
        else:
            return render_template('search_gene.html',form=search)
    return render_template('search_gene.html',form=search)


@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    # fusion("7SK_GARS")
    # gene("7SK")
    # dataset("GSE118389")
    app.run(threaded=True, port=5000)