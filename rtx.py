from bs4 import BeautifulSoup
import requests
from telegraph import Telegraph

def make_view(title,content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='Saidkodirov Tolibjon')
    page = telegraph.create_page(title=f"🌐 {title}", html_content=content)
    instant_view_url = 'https://telegra.ph/{}'.format(page['path'])
    return instant_view_url

def remover(text):
    return text.replace('\n', '')

def sport(q='gainer'):
    url = f"https://blb.uz/uz/search-uz/?search={q}"
    r = requests.get(url)
    doc = BeautifulSoup(r.content, "html.parser")
    images = doc.find_all("img", attrs={"class": "img-fluid", "width": "228"})
    titles = doc.find_all(attrs={"class": "rm-module-title"})
    labels = doc.find_all(attrs={"class": "rm-module-stock"})
    descrs = doc.find_all(attrs={"class": "rm-module-attr"})
    prices = doc.find_all(attrs={"class": "rm-module-price"})
    urls=doc.find_all("a", attrs={"class": "order-0"})
    urls = [url['href'] for url in urls]
    images=[image['src'] for image in images]
    titles=[d.text for d in titles]
    labels=[d.text for d in labels]
    cost=[]
    for price in prices:
        for p in price.children:
            cost.append(p.text)
    dscrs = []
    for des in descrs:
        text = ""
        for d in des.children:
            txt = remover(d.text)
            text+=f"{txt}\n"
        dscrs.append(text)
    products=[]
    for m in range(len(titles)):
        products.append({
            "photo": images[m],
            "title": titles[m],
            "status": labels[m],
            "desc": dscrs[m],
            "price": cost[m],
            "url": urls[m]
        })
    content="Mahsulotlar ro'yxati:<hr> <br>"
    for _p in products:
        photo = _p['photo']
        title = _p['title']
        status = _p['status']
        desc = _p['desc']
        price = _p['price']
        url = _p['url']
        content+=f"<img src='{photo}'><br>"
        content+=f"<p>{title}</p>"
        content+=f"<p>{status}</p>"
        content+=f"<p>{desc}</p>"
        content+=f"<p>Narxi: {price}</p>"
        content+=f"<a href='https://t.me/Saidkodirov'>Sotib olish</a> <br><hr><br>"
    view = make_view(f"{q} - Mahsulotlari", content=content)
    return {
        "products": products,
        "view": view
    }
