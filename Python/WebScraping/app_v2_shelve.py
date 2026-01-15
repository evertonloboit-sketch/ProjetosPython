import requests 
from bs4 import BeautifulSoup
import shelve
import os
import funcoes

# Criar pasta para dados shelve se não existir
pasta_dados = "dados_shelve"
if not os.path.exists(pasta_dados):
    os.makedirs(pasta_dados)

# Caminho completo para o arquivo shelve
arquivo_shelve = os.path.join(pasta_dados, "citacoes.db")

urls = funcoes.retornaUrls(10)
lista = []

for url in urls:
    conteudo = requests.get(url)
    soup = BeautifulSoup(conteudo.text, "html.parser")
    citacoes = soup.find_all("div", class_="quote")
    lista.extend(funcoes.organizaListaCit(citacoes, url))

# Salvar dados no arquivo shelve
with shelve.open(arquivo_shelve) as db:
    # Salvar a lista completa de citações
    db['citacoes'] = lista
    # Salvar também por URL para facilitar acesso posterior
    for url in urls:
        citacoes_url = [item for item in lista if item['Origem'] == url]
        db[f'url_{url}'] = citacoes_url
    # Salvar metadados
    db['total_citacoes'] = len(lista)
    db['total_urls'] = len(urls)
    db['urls_processadas'] = urls

print(f"Dados salvos com sucesso em {arquivo_shelve}")
print(f"Total de citações: {len(lista)}")
