import requests

def get_yaml():
    print("开始获取clash订阅")
    # Исправлен двойной слэш api.dler.io//sub -> api.dler.io/sub
    urls = ["https://api.dler.io/sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_try&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true"]
    
    for i in urls:
        try:
            # Добавлен timeout для защиты воркфлоу от бесконечного зависания
            response = requests.get(i, timeout=15)
            response.raise_for_status()
            
            # Использование современного безопасного менеджека контекста
            with open("output.yaml", 'w', encoding='utf-8') as file_L:
                file_L.write(response.text)
        except requests.RequestException as e:
            print(f"获取订阅 из-за ошибки сети потерпел неудачу: {e}")
            
    print("clash订阅获取完成！")

if __name__ == '__main__':
    get_yaml()
