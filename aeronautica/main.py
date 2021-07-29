import pandas as pd
import pandera as pa
from pandera.checks import Check

df = pd.read_csv('ocorrencia_2010_2020.csv', sep=';', parse_dates=['ocorrencia_dia'], dayfirst=True)

schema = pa.DataFrameSchema(
    coluns= {
        'codigo_ocorrencia': pa.Column(pa.Int),
        'codigo_ocorrencia2': pa.Column(pa.Int),
        'ocorrencia_classificacao': pa.Column(pa.String),
        'ocorrencia_cidade': pa.Column(pa.String),
        'ocorrencia_uf': pa.Column(pa.String, pa.Check.str_length(2, 2)), 
        'ocorrencia_aerodromo': pa.Column(pa.String),
        'ocorrencia_dia': pa.Column(pa.DateTime), 
        'ocorrencia_hora': pa.Column(pa.String, pa.Check.str_matches(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'), nullable=True), #Chek usa uma expressão regular para aceitar somente horas no padrão de 24 horas
        'total_recomendacoes': pa.Column(pa.Int)       
    }
)

schema.validate(df)