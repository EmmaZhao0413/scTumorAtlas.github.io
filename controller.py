from flask import jsonify, request, redirect, render_template
from flask_restful import Resource, reqparse
# from flask_cors import cross_origin
from config import app
from model import *
import numpy as np
# from collections import defaultdict

df = pd.read_pickle('fake.pickle').set_index('Code')
@app.route('/search/results')
def search_database(search):
	results = search_results(
		search.data['cancer_type'],
		search.data['source'],
		search.data['metastasis'],
		search.data['alteration_type']
		)
	return render_template('results.html',tables=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in results],form=search)

# function for filter implementation
# input: filter parameter from selection bars
# output: result table of the course information
def search_results(cancer_type, source, metastasis, alteration_type, n_return=10):
        n_return=int(n_return)
        year=int(year)
        pos_vals = np.zeros((len(df),))
        idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(df.index))),key=lambda x:x[0],reverse=True)]
        tf = df.loc[idxs]
        # requisite_vals = defaultdict(list)
        main_table = tf
        for name,filter in [('Cancer Type',cancer_type), ('Source',source), ('Metastasis',metastasis), ('Alteration Type',alteration_type)]:
                if filter != 'Any':
                        main_table = main_table[main_table[name] == filter]
        tables = [main_table[0:n_return][['dataset name','cancer_type','source','metastasis','alteration_type','publication']]]
        return tables