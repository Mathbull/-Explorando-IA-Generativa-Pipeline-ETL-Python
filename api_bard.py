# Extraia a lista de IDs de usuário a partir do arquivo CSV. Para cada ID, faça uma requisição GET para obter os dados do usuário correspondente.
from bardapi import BardCookies
import os
import pandas as pd
import requests
import json

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

df = pd.read_csv(
    'Explorando IA Generativa em um Pipeline de ETL com Python\SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)


def get_user(id):
    response = requests.get(f"{sdw2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]

# Utilizando a API do Bard para gerar uma mensagem de marketing personalizada para cada usuário.

cookie_dict = {
    "__Secure-1PSID": "aAjTQGB8GSkEAn5fwig8ibx0ImsNagXrUCKSkUnGmL3xL_R60fmHVsOmyQ8S2FxgUYmgoA.",
    "__Secure-1PSIDTS": "sidts-CjEBSAxbGTXQ1nE1RsLLZMhvaP6wEWEpBC_yAcQmpl0n5lJ3t0yGblnusxz0A61I2hdrEAA",
    "__Secure-1PSIDCC": "APoG2W8dPgYoDGPj66G9kQCdRjeTIIOb05gVVGw6aM25ep0Gv9BG5cIUkW1wAxh1Yozn5w20Wnw"
}

bard = BardCookies(cookie_dict=cookie_dict)


def generete_ai_news(user):
    input_text = f"Crie uma pequena mensagem (de no máximo de 100 caracteres) de marketing bancário sobre a importância de investimentos, para o usuário com o nome: {user['name']}"
    completion = bard.get_answer(input_text)['content']
    return completion


for user in users:
    news = generete_ai_news(user)
    # print(news)
    user['news'].append({"icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
                         "description": news
                         })

# print(json.dumps(users, indent=2))

# Atualize a lista de "news" de cada usuário na API com a nova mensagem gerada.


def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}!")
