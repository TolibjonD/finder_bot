from environs import Env
import requests

env = Env()
env.read_env()

API_KEY = env("API_KEY")
SEARCH_ENGINE_ID = env("SEARCH_ENGINE_ID")

        

async def search(text):
    url = 'https://www.googleapis.com/customsearch/v1'
    params={
        'q': text,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        # 'lr': f'lang_{lang_code}',
        # 'gl': 'US'
    }

    response=requests.get(url, params=params)
    results=response.json()
    print(results)
    r_list = []

    if 'items' in results:
        for item in results['items']:
            url = {'title': item['title'], 'snippet': item['snippet'], 'link': item['link'], 'image': False}
            if 'pagemap' in item:
                if 'cse_image' in item['pagemap']:
                    url['image'] = item['pagemap']['cse_image'][0]['src']
            else:
                print("IMAGE NOT FOUND")
            r_list.append(url)
        return r_list
    else:
        return "So'rovingiz bo'yicha hech qanday ma'lumot mavjud emas. Sizning kunlik foydalanish limitingiz yakuniga yetgan bo'lishi ham mumkin."