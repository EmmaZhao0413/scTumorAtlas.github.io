import scanpy as sc
import pandas as pd
# adata = sc.read_h5ad("/home/emmazhao/scTumorAtlas/GSE83142matrices/GSE83142_expr.h5ad")161896
# adata_df = adata.to_df()
# print(adata_df.columns)
df = pd.read_csv("/home/emmazhao/scTumorAtlas/GSE83142matrices/GSE83142_qc_and_labeled_sample_info.csv")
print(df["source_name_ch1"])
