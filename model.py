from wtforms import Form, StringField, SelectField
import pandas as pd
import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import scanpy as sc
from anndata import AnnData
from matplotlib import pyplot as plt
import seaborn as sns
from copy import deepcopy
from ..colorSchemes import color_fusion


def plot_fusion_two_gene_names_umap(fusion_adata, fusion_two_gene_names, title_of_plot, 
                                    two_genes_fusion_0_or_1 = True, color_map='Oranges', **kwargs):
    
    var_on_interest = list(fusion_adata.var[fusion_adata.var['#FusionName'].isin(fusion_two_gene_names)].index)

    feature_mat = pd.DataFrame(fusion_adata.to_df().loc[:,var_on_interest].sum(1))
    feature_mat.columns = [title_of_plot]
    
    if two_genes_fusion_0_or_1:
        feature_mat[title_of_plot][feature_mat[title_of_plot] > 0] = 1

    var_mat = pd.DataFrame([title_of_plot])
    var_mat.columns = ['feature_names']
    var_mat.index = var_mat.feature_names

    plot_feature_adata = AnnData(np.array(feature_mat), obs=fusion_adata.obs,
                                      var=var_mat, uns=fusion_adata.uns, obsm=fusion_adata.obsm, dtype='float64')
    
    plot_feature_adata = process_fusion_data_for_plot(plot_feature_adata, [title_of_plot])
    
    sc.pl.umap(plot_feature_adata, color='fusion_' + title_of_plot, color_map=color_map, **kwargs)
    
    return plot_feature_adata


def plot_cell_counts_for_features(query_df, display_col, save=None, percentage=False, all_df=None, 
                                  show=True, **kwargs):
            
    tmp = query_df[display_col].value_counts()
    tmp = pd.DataFrame(tmp)
    
    if percentage:
        value_meaning = 'Percentage of cells'
        tmp_1 = all_df[display_col].value_counts()
        tmp_1 = pd.DataFrame(tmp_1)

        tmp = tmp / tmp_1.loc[tmp.index]
        tmp.columns = [value_meaning]
        tmp = tmp.sort_values(value_meaning, ascending=False)
    else:
        value_meaning = 'Number of cells'
        tmp.columns = [value_meaning]

    order = list(tmp.index)
    tmp[display_col] = tmp.index
    tmp = tmp.reset_index().head(20)

    fig, ax = plt.subplots(figsize=(len(tmp) / 3, 3))
    ax = sns.barplot(x=display_col, y=value_meaning, data=tmp, order=order, **kwargs)
    for index,row in tmp.iterrows():
        ax.text(row.name,row[value_meaning] + tmp[value_meaning].max()/50,
                round(row[value_meaning],2), color="black", ha="center")
    plt.ylim(0, tmp[value_meaning].max() * 1.1)
    #ax.set_yticklabels(ax.get_yticklabels(), fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=11)
    plt.xlabel('')
    
    if save is not None:
        plt.savefig(save, dpi=600,  bbox_inches='tight')
    if show:
        plt.show()
    plt.close()
    
    return ax


def process_fusion_data_for_plot(fusion_adata, plot_features, color_fusion=color_fusion):
    
    tmp_fusion_adata = deepcopy(fusion_adata)
    tmp_df = tmp_fusion_adata.to_df().loc[:,plot_features]
    tmp_df.columns = 'fusion_' + tmp_df.columns
    tmp_df[tmp_df==0] = 'Without fusion'
    tmp_df[tmp_df==1] = 'With fusion'
    tmp_fusion_adata.obs = pd.concat([fusion_adata.obs, tmp_df], axis=1)
    tmp_fusion_adata.obs = tmp_fusion_adata.obs.astype('category')

    color_fusion = dict([(key, color_fusion[key]) for key in ['With fusion','Without fusion']])
    for i in tmp_df.columns:
        tmp_fusion_adata.uns[i+'_colors'] = list(color_fusion.values())
    
    return tmp_fusion_adata

class DatabaseForm(Form):
    # gene = [
    #     ('Any', 'Any'),
    #     ('ENST001','ENST001'),
    #     ('ENST002','ENST002'),
    #     ('ENST003','ENST003'),
    # ]
    cancer_type = [
        ('Any', 'Any'),
        ('GBM','GBM'),
        ('BRCA','BRCA'),
        ('LCML','LCML'),
        ('OSCC','OSCC'),
        ('SKCM','SKCM'),
        ('CRC','CRC'),
        ('MM','MM'),
        ('ALL','ALL'),
        ('LGG','LGG'),
        ('LUAD','LUAD'),
        ('ESCA','ESCA'),
        ('PRAD','PRAD'),
        ('LIHC','LIHC'),
        ('PAAD','PAAD'),
        ('HCC','HCC'),
        ('KIRC','KIRC'),
        ('LUSC','LUSC')
    ]            
    source = [
        ('Any', 'Any'),
        ('cell line', 'cell line'),
        ('CTC', 'CTC'),
        ('PDX', 'PDX'),
        ('tissue', 'tissue')
    ]           
    metastasis = [
        ('Any', 'Any'),
        ('metastasis', 'metastasis'),
        ('primary', 'primary')
    ]

    gene = StringField('Gene:')
    fusion = StringField('Fusion:')
    cancer_type = SelectField('Cancer Type:', choices=cancer_type)
    source = SelectField('Cancer Source:', choices=source)
    metastasis = SelectField('Metastasis:', choices=metastasis)