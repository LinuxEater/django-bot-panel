import requests
from bs4 import BeautifulSoup
from django.utils import timezone

def scrape_site(url, selector=None):
    """Pega texto de um site. Se selector não for informado, retorna o <title>."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        return "[erro] " + str(e)

    if selector:
        elems = soup.select(selector)
        if not elems:
            return "[elemento não encontrado: " + selector + "]"
        return elems[0].get_text(strip=True) or "[elemento sem texto]"

    title = soup.find("title")
    if title:
        return title.get_text(strip=True)
    return "[<title> não encontrado]"

def send_telegram(token, chat_id, text):
    """Envia mensagem para o Telegram."""
    try:
        r = requests.post(
            "https://api.telegram.org/bot" + token + "/sendMessage",
            data={"chat_id": chat_id, "text": text}
        )
        return r.status_code == 200
    except:
        return False

def now_local():
    """Retorna datetime local (America/Sao_Paulo)."""
    return timezone.localtime(timezone.now())
