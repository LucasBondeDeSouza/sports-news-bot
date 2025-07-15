import telebot
import requests
from bs4 import BeautifulSoup
import os
import time

API_KEY = os.environ.get("TELEGRAM_API_KEY")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(API_KEY)

def extrair_primeira_noticia():
    url = "https://ge.globo.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    requisicao = requests.get(url, headers=headers)

    if requisicao.status_code == 200:
        soup = BeautifulSoup(requisicao.text, "html.parser")
        post = soup.find(class_="feed-post")
        if post:
            title_tag = post.find(class_="feed-post-link")
            description_tag = post.find(class_="feed-post-body-resumo")
            link = title_tag.get("href") if title_tag else None

            mensagem = ""
            if title_tag:
                mensagem += f"📰 *{title_tag.text.strip()}*\n"
            if description_tag:
                mensagem += f"📝 {description_tag.text.strip()}\n"
            if link:
                mensagem += f"🔗 [Leia mais]({link})"

            return link, mensagem
    else:
        print(f"[ERRO] Falha ao acessar o site. Status code: {requisicao.status_code}")
    return None, None

def monitorar_noticias():
    caminho = "ultimo_link.txt"

    # Tenta ler o último link enviado
    ultimo_link_enviado = ""
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            ultimo_link_enviado = f.read().strip()

    link, mensagem = extrair_primeira_noticia()

    if link:
        if link != ultimo_link_enviado:
            print(f"[NOVO] Nova notícia detectada. Enviando para o Telegram...")
            bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
            with open(caminho, "w") as f:
                f.write(link)
            print(f"[OK] Notícia enviada e link salvo.")
        else:
            print(f"[REPETIDA] Nenhuma nova notícia. Link já enviado anteriormente.")
    else:
        print(f"[ERRO] Não foi possível extrair a notícia.")

while True:
    print(f"\n[LOG] Verificando por novas notícias... {time.strftime('%Y-%m-%d %H:%M:%S')}")
    monitorar_noticias()
    time.sleep(300)  # Espera 5 minutos