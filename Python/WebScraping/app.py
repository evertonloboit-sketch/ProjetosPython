import requests 
from bs4 import BeautifulSoup
import pandas as pd

url = "https://quotes.toscrape.com/"
conteudo = requests.get(url)

#escrever = open("quotes.txt", "w", encoding="utf-8")
#for linha in conteudo.text:
#    escrever.write(linha)
#escrever.close()

soup = BeautifulSoup(conteudo.text, "html.parser")
citacoes = soup.find_all("div", class_="quote")

#frase = citacoes[0].find("span",class_="text").get_text()
#print(frase)

lista = []
for citacao in citacoes:
    frase = citacao.find("span",class_="text").get_text()
    autor = citacao.find("small",class_="author").get_text()
    #tags = citacao.find("div",class_="tags").get_text()
    lista.append({"Citação":frase,"Autos":autor})

#print(lista)

df = pd.DataFrame(lista)
df.to_csv("citacoes.csv",index=False,encoding="utf-8")