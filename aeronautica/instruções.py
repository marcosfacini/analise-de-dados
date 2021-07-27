import pandas as pd
import pandera as pa
from pandera.checks import Check

# todas as alterações estão sendo feitas no dataframe criado e não no arquivo de origem

# a separação de colunas padrão no csv é a virgula
# só que o arquivo 'ocorrencia_2010_2020;csv' está usando ponto e vírgula como separador de colunas
# op parametro sep=# altera a separação das colunas para ponto e virgula
# parametro parse_dates transforma a coluna ocorrencia_dia que era string em um formato de data para poder ser manipulado como data
# parametro dayfirts=True faz com que na coluna de data o primeiro valor seja o dia para manter o padrão brasileiro
df = pd.read_csv('aeronautica\ocorrencia_2010_2020.csv', sep=';', parse_dates=['ocorrencia_dia'], dayfirst=True)

# fazendo a validação do dataframe atraves de um esquema para tratar possiveis erros
schema = pa.DataFrameSchema(
    columns= {
        'codigo_ocorrencia': pa.Column(pa.Int), # dá erro se colocar uma string
        'codigo_ocorrencia2': pa.Column(pa.Int),
        'ocorrencia_classificacao': pa.Column(pa.String),
        'ocorrencia_cidade': pa.Column(pa.String),
        'ocorrencia_uf': pa.Column(pa.String, pa.Check.str_length(2,2)), # aceita o maximo e o minimo de 2 caracteres
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

# para selecionar um unico campo da tabela
# .loc[numero-da-linha, nome-da-coluna]
# print (df.loc[1,'ocorrencia_cidade'])

# visualisando dados apenas da linha 1 
# print (df.loc[1])

# visualisando dados da linha 1 até a linha 3
# print (df.loc[1:3])

# mostrar apenas linha 10 e linha 40, colocando os numeros das linhas dentro de uma lista
# df.loc[[10,40]]

# mostrar coluna inteira
# df.loc[:,'ocorrencia_cidade']

# verificando se existe duplicidade nos valores da coluna
# df.codigo_ocorrencia.is_unique

# coluna codigo_ocorrencia passou a ser o indice que indica o numero das linhas
# parametro inplace faz a alteração no dataframe (df) local
# df.set_index('codigo_ocorrencia', inplace=True)
# print (df.loc[40324])

# resetando para o index padrão
# df.reset_index(drop=True, inplace=True)

# mudando simbolo incorreto da linha 0 da coluna ocorrencia_aerodromo para um campo vazio
# df.loc[0,'ocorrencia_aerodromo'] = ''

# mudando todos os valores da linha 1 para receber o numero 20
# df.loc[1] = 20

# mudando todos os valore da coluna total_recomendacoes para receber o numero 10
# df.loc[:,'total_recomendacoes'] = 10

# criando uma nova coluna chamada ocorrencia_uf_bkp que vai receber os dados da coluna ocorrencia_uf
# fazemos isso para criar um backup da coluna ocorrencia_uf para podermos alterar os dados nela agora, sem perder as informações originais
# df['ocorrencia_uf_bkp'] = df.ocorrencia_uf

# aonde a coluna ocorrencia_uf for SP, a coluna ocorrencia_classificacao receberá a palavra GRAVE
# df.loc[df.ocorrencia_uf == 'SP', ['ocorrencia_classificacao']] = 'GRAVE'
# print (df.loc[df.ocorrencia_uf == 'SP'])









