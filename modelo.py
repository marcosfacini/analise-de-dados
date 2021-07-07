import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# lendo o banco de dados
dados = pd.read_csv('train.csv')
# print (dados.head())

# retirando colunas com o a função .drop()
# axis = 1 significa para retirar colunas com esses nomes
dados = dados.drop(['Name', 'Ticket', 'Cabin', 'Embarked'], axis = 1)
# print (dados.head())

# transformando o index(numero das linhas) na coluna PassengerId, ela se tornou o index agora
dados = dados.set_index(['PassengerId'])
# print (dados.head())

# renomeando a coluna survived para target 
# quendo o parametro inplace recebe False retorna uma cópia modificada
dados = dados.rename(columns= {'Survived': 'target'}, inplace = False)
# print (dados.head())

# estatistica descritiva
# por padrão só vai analisar as colunas que tenham numeros
# print (dados.describe())

# fazendo a analise da coluna sexo que é uma string
# print (dados.describe(include=['O']))

# transformando os dados da coluna sexo que estão em string em numeros
# criando uma coluna chamada Sexo que vai receber os dados da coluna Sex e transforma-los em 0 e 1
# parametros: aonde aparecer a palavra female, será substituido por 1, caso contrario receberá 0
# zero vale masculino e 1 vale feminino
dados['Sexo'] = np.where(dados['Sex'] == 'female', 1, 0)
# print (dados.head())

# seguindo o mesmo esquema do sexo(modelo acima) criando 3 novas colunas que vão receber os valores de uma unica coluna
# parametros: aonde aparecer o numero 1, receberá o valor 1 tambem, caso contrario receberá 0
dados['Pclass_1'] = np.where(dados['Pclass'] == 1, 1, 0)
# aonde aparecer o numero 2, será substituido por 1, caso contrario receberá 0
dados['Pclass_2'] = np.where(dados['Pclass'] == 2, 1, 0)
# aonde aparecer o numero 3, será substituido por 1, caso contrario receberá 0
dados['Pclass_3'] = np.where(dados['Pclass'] == 3, 1, 0)

# retirando as colunas que ja tiveram os seus dados tranformadas acima, para não confundir
dados = dados.drop(['Sex', 'Pclass'], axis = 1)
# print (dados.head())

# mostrando a soma de quantos campos vazios cada coluna possui
# print (dados.isnull().sum())

# substituindo os campos vazios/missing por 0
# se o parametro inplace receber True modifica tambem no arquivo original???? nao entendi bem ainda
dados.fillna(0, inplace = True)
# print (dados.isnull().sum())



# AMOSTRAGEM 
x_train, x_test, y_train, x_test = train_test_split(dados.drop(['target'], axis = 1),
                                                    dados['target'],
                                                    test_size = 0.3,
                                                    random_state = 1234)

# print ([{'treino': x_train.shape}, {'teste': x_test.shape}])


rndforest = RandomForestClassifier(n_estimators= 1000,
                                    criterion= 'gini',
                                    max_depth= 5)

rndforest.fit(x_train, y_train)

probabilidade = rndforest.predict_proba(dados.drop('target', axis=1))[:,1]
classificacao = rndforest.predict(dados.drop('target', axis=1))

# print (probabilidade)
# print (classificacao)

# criando duas colunas novas e colocando o valor das variaveis dentro delas
dados['probabilidade'] = probabilidade
dados['classificacao'] = classificacao

# por padrão a probabilidade acima de 0.5 recebe como classificao o 1 e abaixo de 0.5 como 0
print (dados)








