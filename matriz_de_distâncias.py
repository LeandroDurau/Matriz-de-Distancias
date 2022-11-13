# -*- coding: utf-8 -*-
"""Matriz de Distâncias.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bih8mUJdVsYVPWFdQgJpLRnPmUp0zowe

#Corpus

Sua  tarefa  será  transformar  um  conjunto  de  5  sites,  sobre  o  tema  de  processamento  de 
linguagem natural em um conjunto de cinco listas distintas de sentenças. Ou seja, você fará uma função 
que, usando a biblioteca Beautifull Soap, faça a requisição de uma url, e extrai todas as sentenças desta 
url. Duas condições são importantes:  
>  a) A página web (url) deve apontar para uma página web em inglês contendo, não menos que 1000 palavras.  

> b) O texto desta página deverá ser transformado em um array de senteças.  
 
Para separar as sentenças você pode usar os sinais de pontuação ou as funções da biblibioteca 
Spacy.
"""

import requests
import spacy
import bs4
from bs4 import BeautifulSoup

def adiciona_site(site, lista):

  page = requests.get(site)
  if  not 200==page.status_code:
    print("Site: "+site+" não abriu")
    print(page.status_code)
    return lista
  soap = BeautifulSoup(page.content, 'html.parser')

  spaci = spacy.load('en_core_web_sm')

  
  for i in soap.find_all('p'):
    espaco = spaci(i.get_text())
    for j in espaco.sents:
      lista.append(j)
  return lista

sentencas = []
sentencas1 = adiciona_site("https://www.techtarget.com/searchenterpriseai/definition/natural-language-processing-NLP", [])
sentencas2 = adiciona_site("https://www.sas.com/en_us/insights/analytics/what-is-natural-language-processing-nlp.html#world", [])
sentencas3 = adiciona_site("https://monkeylearn.com/natural-language-processing/", [])
sentencas4 = adiciona_site("https://hbr.org/2022/04/the-power-of-natural-language-processing", [])
sentencas5 = adiciona_site("https://www.oracle.com/artificial-intelligence/what-is-natural-language-processing/", [])
sentencas.append(sentencas1)
sentencas.append(sentencas2)
sentencas.append(sentencas3)
sentencas.append(sentencas4)
sentencas.append(sentencas5)
print(sentencas)

"""#Bag of Words

Sua tarefa será  gerar a matriz termo documento, dos documentos recuperados da internet e 
imprimir esta matriz na tela. Para tanto: 
>a) Considere que todas as listas de sentenças devem ser transformadas em listas de vetores, 
onde cada item será uma das palavras da sentença. 

>b) Todos  os  vetores  devem  ser  unidos  em  um  corpus  único  formando  uma  lista  de  vetores, 
onde cada item será um lexema. 

>c) Este único corpus será usado para gerar o vocabulário. 

>d) O  resultado  esperado  será  uma  matriz  termo  documento  criada  a  partir  da  aplicação  da 
técnica bag of Words em todo o corpus. 
"""

def adiciona_palavra_bag (sentencas, bag, doc,tamanho_doc,x,y):
  palavra = sentencas[x][y]
  #removedor de espaços  ®
  if palavra.dep_ == "SPACE" or palavra.dep_ == "dep" or palavra.dep_ == "punct":
    excecoes = ["referred","hinges","have","so","am","recall","'d"]
    if not palavra.text in excecoes:
      return bag
  achei = False
  for i in bag:
    if i[0].text == palavra.text:
      achei = True
      i[doc] += 1

  if achei:
    return bag
  bag.append([palavra])
  for i in range(tamanho_doc):
    bag[len(bag)-1].append(0)
  bag[len(bag)-1][doc] = 1
  return bag

corpus = []
doc = -1
for i in sentencas:
  for j in i:
    if len(j) == 1 and j[0].dep_ == "dep":
      continue
    doc += 1
    corpus.append([])
    for k in j:
      corpus[doc].append(k)

bag = []
#spacy.displacy.render(sentencas1[9], style="dep", jupyter = True)
for i in range(len(corpus)):
  for j in range(len(corpus[i])):
    bag = adiciona_palavra_bag(corpus,bag,i+1,len(corpus),i,j)

# bag muito grande para printar inteiro

print(len(bag))
print(bag [100])

"""#TF - IDF

>Sua  tarefa  será  gerar  a  matriz  termo-documento  usando  TF-IDF  por  meio  da  aplicação  das 
fórmulas TF-IDF na matriz termo-documento criada com a utilização do algoritmo Bag of Words. Sobre 
o Corpus que recuperamos anteriormente. 
"""

import numpy as np

def criaMatrizTF(bag):
  tf = []
  bagt = np.transpose(bag)

  for i in bagt[0]:
    tf.append([i])
  for i in range(1,len(bagt)):
    num_palavras = 0
    num_palavras = np.sum(bagt[i])
    for j in range(len(bagt[0])):
      tf[j].append(bagt[i][j]/num_palavras)
  return tf


def criaMatrizIDF(bag):
  idf = []
  num_docs = len(bag[0]) - 1
  for i in range(len(bag)):
    idf.append([bag[i][0]])
    num_termos = 0
    for j in range(1, len(bag[0])):
      if  bag[i][j] != 0:
        num_termos += 1
    idf[i].append(np.log(num_docs/num_termos))
  return idf

def criaMatrizTF_IDF(tf, idf):
  tf_idf = []
  for i in range(len(tf)):
    tf_idf.append([tf[i][0]])
    for j in range(1,len(tf[0])):
      tf_idf[i].append(tf[i][j]*idf[i][1])
  return tf_idf




tf_final = criaMatrizTF(bag)
print(len(tf_final))
for i in range(25):
  print(tf_final[i])
idf_final = criaMatrizIDF(bag)
print(len(idf_final))
for i in range(25):
  print(idf_final[i])
tf_idf_final = criaMatrizTF_IDF(tf_final,idf_final)
print(len(tf_idf_final))
for i in range(25):
  print(tf_idf_final[i])

"""#Matriz de Distâncias
>Sua tarefa será gerar uma matriz de distância, computando o cosseno do ângulo entre todos os
vetores que encontramos usando o tf-idf. Para isso use a seguinte fórmula para o cálculo do cosseno
use a fórmula apresentada em Word2Vector (frankalcantara.com)
(https://frankalcantara.com/Aulas/Nlp/out/Aula4.html#/0/4/2) e apresentada na figura a seguir: 

>O resultado deste trabalho será uma matriz que relaciona cada um dos vetores já calculados com todos os outros vetores disponíveis na matriz termo-documento
"""

def vetorizacao(tf_idf):
  vetores = []
  for i in range(len(tf_idf)):
    vetores.append([tf_idf[i][0]])
    for j in range(len(tf_idf)):
      vetores[i].append(0.0)

  for i in range(len(tf_idf)):
    for j in range(i,len(tf_idf)):
      cos_sim = 1.0
      if i!=j:
        cos_sim = np.dot(tf_idf[i][1:],tf_idf[j][1:])/(np.linalg.norm(tf_idf[i][1:])*np.linalg.norm(tf_idf[j][1:]))
        vetores[j][i+1] = cos_sim
      vetores[i][j+1] = cos_sim
  return vetores

vetores_final = vetorizacao(tf_idf_final)
for i in range(25):
  print(vetores_final[i])