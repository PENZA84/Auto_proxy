import requests
import re

try_sub = []
e_sub = []

def test_cfmem():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    try:
        # 1. Запрашиваем страницу со всеми бесплатными статьями
        res = requests.get("https://www.cfmem.com/search/label/free", headers=headers, timeout=10)
        res.raise_for_status()
        
        # Находим ВЕЕ ВСЕ ссылки, похожие на статьи с датами
        all_matches = re.findall(r"https?://www\.cfmem\.com/\d{4}/\d{2}/[^\"'\s>]+?\.html", res.text)
        
        # Фильтруем: убираем старую инструкцию-руководство из 2021 года
        article_urls = [url for url in all_matches if "v2rayng.html" not in url]
        
        if not article_urls:
            print("Ошибка: ссылка на свежую статью на cfmem.com не найдена.")
            return
            
        # Берем самую первую (актуальную) ссылку из оставшихся
        article_url = article_urls[0]
        print(f"Найдена ссылка на свежую статью: {article_url}")
        
        # 2. Переходим внутрь найденной свежей статьи
        res = requests.get(article_url, headers=headers, timeout=10)
        res.raise_for_status()
        
        # Ищем тег с самой ссылкой на подписку v2ray внутри статьи
        sub_match = re.search(r'>v2ray订阅链接&#65306;(.*?)</span>', res.text)
        if not sub_match:
            print("Ошибка: ссылка на подписку внутри статьи cfmem.com не найдена.")
            return
            
        sub_url = sub_match.group(1)
        print(f"Успешно найден URL подписки: {sub_url}")
        
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取cfmem.com成功！")
        
    except requests.RequestException as req_err:
        print(f"Сетевая ошибка при работе с cfmem.com: {req_err}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        print("获取cfmem.com失败！")

if __name__ == '__main__':
    test_cfmem()
