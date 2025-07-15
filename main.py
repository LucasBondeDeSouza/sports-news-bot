import telebot
import requests
from bs4 import BeautifulSoup
import os

API_KEY = os.environ.get("TELEGRAM_API_KEY")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(API_KEY)

# Armazenar o link da última notícia enviada
ultimo_link_enviado = ""

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
    return None, None

def monitorar_noticias():
    caminho = "ultimo_link.txt"
    ultimo_link_enviado = ""

    # Tenta ler o último link enviado
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            ultimo_link_enviado = f.read().strip()

    link, mensagem = extrair_primeira_noticia()
    if link and link != ultimo_link_enviado:
        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
        # Salva o novo link
        with open(caminho, "w") as f:
            f.write(link)

# Inicia o monitoramento contínuo
monitorar_noticias()