from wtforms import Form, StringField, SelectField
import pandas as pd


class DatabaseForm(Form):
    cancer_type = [
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
        ('cell line', 'cell line'),
        ('CTC', 'CTC'),
        ('PDX', 'PDX'),
        ('tissue', 'tissue')
    ]           
    metastasis = [
        ('metastasis', 'metastasis'),
        ('primary', 'primary')
    ]
    alteration_type = [
        ('SNV','SNV'),
        ('CNV','CNV'),
        ('Splicing','Splicing'),
        ('Gene Fusion','Gene Fusion')
    ]

    cancer_type = SelectField('Cancer Type:', choices=cancer_type)
    source = SelectField('Cancer Source:', choices=source)
    metastasis = SelectField('Metastasis:', choices=metastasis)
    alteration_type = SelectField('Alteration Type:', choices=alteration_type)