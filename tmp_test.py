import scanpy as sc
import pandas as pd
import csv
# adata = sc.read_h5ad("/home/emmazhao/scTumorAtlas/GSE83142matrices/GSE83142_expr.h5ad")161896
# adata_df = adata.to_df()
# print(adata_df.columns)
# df = pd.read_csv("/home/emmazhao/scTumorAtlas/GSE83142matrices/GSE83142_qc_and_labeled_sample_info.csv")
# print(df["source_name_ch1"])


# output_list=[]
# reader_neo = csv.reader(open('/home/emmazhao/scTumorAtlas/data/gencode_v19_gene_info.csv'), delimiter=",")
# fields = next(reader_neo)
# for line in reader_neo:
#     gene_id=line[0]
#     gene_link="<a href=/gene/"+gene_id+">"+gene_id+"</a>"
#     line.append(gene_link)
#     output_list.append(line)
# fields.append("gene_link")
# # print(fields)
# data=pd.DataFrame(output_list)
# print(data.columns)
# data.columns=fields
# data.to_csv("gene_info_output.csv",header=1,sep=',',index=0)


# output_list=[]
# reader_neo = csv.reader(open('/home/emmazhao/scTumorAtlas/data/general_table_for_all_datasets_with_reference_new_for_Emma_0527.csv'), delimiter=",")
# fields = next(reader_neo)
# for line in reader_neo:
#     dataset_id=line[0]
#     dataset="<a href=/dataset/"+dataset_id+">"+dataset_id+"</a>"
#     line.append(dataset)
#     output_list.append(line)
# fields.append("dataset_id")
# data=pd.DataFrame(output_list)
# print(data.columns)
# data.columns=fields
# data.to_csv("dataset_info_output.csv",header=1,sep=',',index=0)



output_list=[]
reader_neo = csv.reader(open('/home/emmazhao/scTumorAtlas/data/used_general_fusion_info_0529.csv'), delimiter=",")
fields = next(reader_neo)
for line in reader_neo:
    fusion_id=line[1]
    fusion_1=fusion_id.strip().split('--')[0]
    fusion_2=fusion_id.strip().split('--')[1]
    fusion_link="<a href=/fusion/"+fusion_1+"_"+fusion_2+">"+fusion_id+"</a>"
    line.append(fusion_link)
    output_list.append(line)
fields.append("fusion_link")
data=pd.DataFrame(output_list)
data.columns=fields
data.to_csv("fusion_info_output.csv",header=1,sep=',',index=0)