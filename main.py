import telebot
import requests
from bs4 import BeautifulSoup
import os

API_KEY = os.environ.get("TELEGRAM_API_KEY")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(API_KEY)

# Pegar notícia mais recente
def extrair_primeira_noticia():
    url = "https://ge.globo.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    requisicao = requests.get(url, headers=headers)

    if requisicao.status_code == 200:
        pagina = BeautifulSoup(requisicao.text, "html.parser")
        news = pagina.find(class_="feed-post-link")
        title = news.text.strip()
        link = news['href']

        return title, link


# Veríficar se a noticia já foi enviada
def verificar_noticia_enviada(link):
    # Lendo o arquivo .txt
    with open('ultimo_link.txt', 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f]
        # Verificando se a notícia já existe no arquivo .txt
        if link in linhas:
            return True
        else:
            return False


# Enviar Mensagem
def send_message():
    title, link = extrair_primeira_noticia()
    if verificar_noticia_enviada(link):
        print("Notícia Repetida")
    else:
        print("Notícia Enviada!")
        # Adicionando uma nova notícia ao final do arquivo .txt
        with open('ultimo_link.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'{link}\n')

        # Montando a mensagem para o bot enviar pelo telegram
        message = ""
        if title:
            message += f"📰 *{title}*\n"
        if link:
            message += f"🔗 [Leia mais]({link})"

        # Bot enviando a mensagem pelo telegram
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")


# Executar a função de enviar mensagem
send_message()