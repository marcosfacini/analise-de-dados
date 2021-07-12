import pandas as pd
import pandera as pa
from pandera.checks import Check

# a separação de colunas padrão no csv é a virgula
# só que o arquivo 'ocorrencia_2010_2020;csv' está usando ponto e vírgula como separador de colunas
# op parametro sep=# altera a separação das colunas para ponto e virgula
# parametro parse_dates transforma a coluna ocorrencia_dia que era string em um formato de data para poder ser manipulado como data
# parametro dayfirts=True faz com que na coluna de data o primeiro valor seja o dia para manter o padrão brasileiro
df = pd.read_csv('ocorrencia_2010_2020.csv', sep=';', parse_dates=['ocorrencia_dia'], dayfirst=True)

# fazendo a validação do dataframe atraves de um esquema para tratar possiveis erros
schema = pa.DataFrameSchema(
    coluns= {
        'codigo_ocorrencia': pa.Column(pa.Int), # dá erro se colocar uma string
        'codigo_ocorrencia2': pa.Column(pa.Int),
        'ocorrencia_classificacao': pa.Column(pa.String),
        'ocorrencia_cidade': pa.Column(pa.String),
        'ocorrencia_uf': pa.Column(pa.String, pa.Check.str_length(2, 2)), # aceita o maximo e o minimo de 2 caracteres
        'ocorrencia_aerodromo': pa.Column(pa.String),
        'ocorrencia_dia': pa.Column(pa.DateTime), # dá erro se for colocada uma data inválida
        'ocorrencia_hora': pa.Column(pa.String, pa.Check.str_matches(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'), nullable=True), #Chek usa uma expressão regular para aceitar somente horas no padrão de 24 horas
        'total_recomendacoes': pa.Column(pa.Int)       # parametro nullable=True permite colunas vazias sem dar erro
    }
)

schema.validate(df)

# metodo head() por padrão printa somente as 5 primeiras linhas
# mas pode-se passar a quantidade de linhas como parametro
# print (df.head(10))

# metodo tail() por padrão printa somente as 5 ultimas linhas
# mas pode-se passar a quantidade de linhas como parametro
# print (df.tail(7))

# metodo dtypes mostra qual é o tipo de dado de cada coluna
# print (df.dtypes)

# mostrando apenas uma coluna
# print (df.ocorrencia_dia)

# mostrando apenas o mes
# print (df.ocorrencia_dia.dt.month)









