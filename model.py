from wtforms import Form, StringField, SelectField
import pandas as pd


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
    cancer_type = SelectField('Cancer Type:', choices=cancer_type)
    source = SelectField('Cancer Source:', choices=source)
    metastasis = SelectField('Metastasis:', choices=metastasis)