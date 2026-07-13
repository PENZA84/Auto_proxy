import requests
import re

try_sub = []
e_sub = []

def test_cfmem():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
    }
    try:
        # 1. Запрашиваем страницу категории
        res = requests.get("https://www.cfmem.com/search/label/free", headers=headers, timeout=10)
        res.raise_for_status()
        
        # Безопасный поиск ссылки на статью
        article_match = re.search(r"https?://www\.cfmem\.com/\d{4}/\d{2}/\S+v2rayclash-vpn.html", res.text)
        if not article_match:
            print("Ошибка: Ссылка на статью на cfmem.com не найдена.")
            return
            
        article_url = article_match.group()
        
        # 2. Запрашиваем страницу самой статьи
        res = requests.get(article_url, headers=headers, timeout=10)
        res.raise_for_status()
        
        # Безопасный поиск ссылки на подписку
        sub_match = re.search(r'>v2ray订阅链接&#65306;(.*?)</span>', res.text)
        if not sub_match:
            print("Ошибка: Ссылка на подписку внутри статьи cfmem.com не найдена.")
            return
            
        sub_url = sub_match.group(1)
        print(f"Успешно найден URL: {sub_url}")
        
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
