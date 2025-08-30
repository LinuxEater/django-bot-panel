import requests
from bs4 import BeautifulSoup

url = "https://hni-scantrad.net/"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

el = soup.select_one("a.text-wrap")
print(el)          # Verifica se encontrou algum elemento
print(r.text[:500])  # Mostra os primeiros 500 caracteres do HTML
