import pandas as pd
import pandera as pa
from pandera.checks import Check

# todas as alterações estão sendo feitas no dataframe criado e não no arquivo de origem

# a separação de colunas padrão no csv é a virgula
# só que o arquivo 'ocorrencia_2010_2020;csv' está usando ponto e vírgula como separador de colunas
# op parametro sep=# altera a separação das colunas para ponto e virgula
# parametro parse_dates transforma a coluna ocorrencia_dia que era string em um formato de data para poder ser manipulado como data
# parametro dayfirts=True faz com que na coluna de data o primeiro valor seja o dia para manter o padrão brasileiro
# parametro na_values transforma todos os dados da variavel valores_ausentes em N/A/N (not a numeric) que tem basicamente o mesmo objetivo do N/A (not avaliable)
valores_ausentes = ['**','###!','####','****','*****','NULL']
df = pd.read_csv("aeronautica\ocorrencia_2010_2020.csv", sep=";", parse_dates=['ocorrencia_dia'], dayfirst=True, na_values=valores_ausentes)


# fazendo a validação do dataframe atraves de um esquema para tratar possiveis erros
schema = pa.DataFrameSchema(
    columns= {
        'codigo_ocorrencia': pa.Column(pa.Int), # dá erro se colocar uma string
        'codigo_ocorrencia2': pa.Column(pa.Int),
        'ocorrencia_classificacao': pa.Column(pa.String),
        'ocorrencia_cidade': pa.Column(pa.String),
        'ocorrencia_uf': pa.Column(pa.String, pa.Check.str_length(2,2), nullable=True), # aceita o maximo e o minimo de 2 caracteres
        'ocorrencia_aerodromo': pa.Column(pa.String, nullable=True),
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
# ou simplesmente:
# df['ocorrencia_cidade']

# localizar por indice com o iloc
# mostrando o ultima linha da tabela
# df.iloc[-1]

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

# mudando aonde aparece os 4 asteristicos na coluna ocorrencia_aerodromo para o valor NA (not avaliable)
# df.loc[df.ocorrencia_aerodromo == '****', ['ocorrencia_aerodromo']] = pd.NA

# fazendo todas as alterações de campos inválidos por N/A de uma só vez
# df.replace(['**','###!','####','****','*****','NULL'], pd.NA, inplace=True)

# somando quantos dados NA (not avaliable) tem por coluna
# df.isna().sum()

# isnull() faz uma função similar ao isna() mostrando a soma dos campos com dados vazios
# df.isnull().sum()

# filtrar somente os campos nulos da coluna ocorrencia_uf
# filtro = df.ocorrencia_uf.isnull()
# df.loc[filtro]

# função count() por padrão não contabiliza campos nulos
# df.count()

# substituindo todos os campos NA pelo numero 10
# df.fillna(10, inplace=True)

# substituir todos os campos aonde aparece o numero 10 pelo NA
# df.replace([10], pd.NA, inplace=True)
# o problema é que nesse caso, acabou alterando os valores da coluna total_recomendacoes que já possuiam o valor 10
# para resolver pode-se alterar novamente só os dados dessa coluna, voltando para o valor padrão
# df.fillna(value={'total_recomendacoes':10}, inplace=True)

# criando uma coluna de backup para poder fazer alterações na coluna original sem se preocupar
# df['total_recomendacoes_bkp'] = df.total_recomendacoes
# depois que ver que as alterações deram certo, pode-se excluir a coluna de backup com a função drop()
# porem a função drop() por padrão apaga linhas com o parametro axis(eixo) setado no 0 
# axis=0 representa linha e axis=1 representa coluna
# df.drop(['total_recomendacoes_bkp'], axis=1, inplace=True)

# função dropna() exclui todas as linhas em que houver campos NA
# df.dropna()
# deve-se ter cuidado, porque não se exclui apenas o campo que é NA, mas a linha inteira a qual ele pertence
# pide-se escolher de qual coluna vai ser excluida a linha com o parametro subset=
# df.dropna(subset=['ocorrencia_uf'])

# excluir linhas duplicadas
# df.drop_duplicates(inplace=True)

# filtro de ocorrências com mais de 10 recomendações
# filtro = df.total_recomendacoes > 10
# df.loc[filtro]

# # filtro que mostra somente duas colunas das linhas em que existem corrências com mais de 10 recomendações
# filtro = df.total_recomendacoes > 10
# df.loc[filtro, ['ocorrencia_cidade', 'total_recomendacoes']]

#ocorrências cuja classificação == INCIDENTE GRAVE	
# filtro = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
# df.loc[filtro]

#ocorrências cuja classificação == INCIDENTE GRAVE e o estado == SP
# filtro1 = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
# filtro2 = df.ocorrencia_uf == 'SP'
# df.loc[filtro1 & filtro2]

#ocorrências cuja classificação == INCIDENTE GRAVE ou o estado == SP
# filtro1 = df.ocorrencia_classificacao == 'INCIDENTE GRAVE'
# filtro2 = df.ocorrencia_uf == 'SP'
# df.loc[filtro1 | filtro2]

#ocorrências cuja (classificação == INCIDENTE GRAVE ou classificação == INCIDENTE) e o estado == SP
# filtro1 = df.ocorrencia_classificacao.isin(['INCIDENTE GRAVE', 'INCIDENTE'])
# filtro2 = df.ocorrencia_uf == 'SP'
# df.loc[filtro1 & filtro2]

#ocorrências cuja cidade comecem com a letra C
# filtro = df.ocorrencia_cidade.str[0] == 'C'
# df.loc[filtro]

#ocorrências cuja cidade terminam com a letra A
# filtro = df.ocorrencia_cidade.str[-1] == 'A'
# df.loc[filtro]

#ocorrências cuja cidade terminam com os caracteres MA
# filtro = df.ocorrencia_cidade.str[-2:] == 'MA'
# df.loc[filtro]

#ocorrências cuja cidade contém (em qualquer parte do conteúdo) os caracteres MA ou AL
# filtro = df.ocorrencia_cidade.str.contains('MA|AL')
# df.loc[filtro]

#ocorrências do ano de 2015
# filtro = df.ocorrencia_dia.dt.year == 2015
# df.loc[filtro]

#ocorrências do ano de 2015 e mês 12 e dias entre 3 e 8
# filtro_ano = df.ocorrencia_dia.dt.year == 2015
# filtro_mes = df.ocorrencia_dia.dt.month == 12
# filtro_dia_inicio = df.ocorrencia_dia.dt.day > 2 
# filtro_dia_fim = df.ocorrencia_dia.dt.day < 9
# df.loc[filtro_ano & filtro_mes & filtro_dia_inicio & filtro_dia_fim]

# criando uma coluna nova que vai unir as colunas ocorrencia_dia com a coluna ocorrencia_hora
# primeiro usar o metodo astype(str) para transformar a coluna ocorrencia_dia para o formato string para poder concatenar com a coluna ocorrencia_hora que já está no formato string
# depois usar a função pd.to_datetime() do pandas para transformar tudo no formato datetime
# df['ocorrencia_dia_hora'] = pd.to_datetime(df.ocorrencia_dia.astype(str) + ' '  + df.ocorrencia_hora)

# filtro por dia e hora
# filtro1 = df.ocorrencia_dia_hora >= '2015-12-03 11:00:00'
# filtro2 = df.ocorrencia_dia_hora <= '2015-12-08 14:30:00'
# df.loc[filtro1 & filtro2]

# in 38








