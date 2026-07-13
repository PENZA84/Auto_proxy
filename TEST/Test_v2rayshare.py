import requests
import re

try_sub = []
e_sub = []

def test_v2rayshare():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
    }
    try:
        # Запрос главной страницы
        res = requests.get("https://v2rayshare.com/", headers=headers, timeout=10)
        res.raise_for_status()
        
        # Безопасный поиск ссылки на свежую статью
        article_match = re.search(r'https://v2rayshare.com/p/\d+\.html', res.text)
        if not article_match:
            print("Ошибка: Ссылка на статью на главной странице v2rayshare.com не найдена.")
            return
            
        article_url = article_match.group()
        
        # Запрос страницы найденной статьи
        res = requests.get(article_url, headers=headers, timeout=10)
        res.raise_for_status()
        
        # Безопасный поиск пути к файлу подписки
        sub_match = re.search(r'<p>https://v2rayshare.com/wp-content/uploads/(.*?)</p>', res.text)
        if not sub_match:
            print("Ошибка: Ссылка на файл подписки внутри статьи не найдена.")
            return
            
        sub_url = 'https://v2rayshare.com/wp-content/uploads/' + sub_match.group(1)
        print(f"Успешно найден URL: {sub_url}")
        
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取v2rayshare.com成功！")
        
    except requests.RequestException as req_err:
        print(f"Сетевая ошибка при работе с v2rayshare.com: {req_err}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == '__main__':
    test_v2rayshare()
