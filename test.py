from telegraph import Telegraph
from bs4 import BeautifulSoup
import requests

def instant_view(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').get_text()
    telegraph = Telegraph()
    telegraph.create_account(short_name='Your Name')

    content = f"<p>Batafsil ma'lumot olish uchun rasmiy sahifaga o'tish kerak</p><br>"
    content = f"<p>Xatolik haqida habar berish uchun: <a href='https://t.me/Saidkodirov'>Admin</a></p><br>"
    content += f"<a href='{url}'>Rasmiy sahifa</a>"

    page = telegraph.create_page(f'🌐 {title}', html_content=content)

    instant_view_url = 'https://telegra.ph/{}'.format(page['path'])
    return instant_view_url