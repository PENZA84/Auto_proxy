import re
import requests
import random, string

e_sub = []

# 获取机场试用订阅
def get_sub_url():
    V2B_REG_REL_URL = '/api/v1/passport/auth/register'
    home_urls = (
        'https://www.ckcloud.xyz',
        'https://fastestcloud.xyz',
        'https://user.bafang.vip',
        'https://cloud.hhygj.xyz',
        'https://feiniaoyun.top',
        'https://www.dgycom.com',
    )
    times = 1
    for current_url in home_urls:
        i = 0
        while i < times:
            header = {
                'Referer': current_url,
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            form_data = {
                'email': ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12)) + '@gmail.com',
                'password': 'autosub_v2b',
                'invite_code': '',
                'email_code': ''
            }
            try:
                response = requests.post(current_url + V2B_REG_REL_URL, data=form_data, headers=header, timeout=10)
                if response.status_code == 200:
                    res_data = response.json()
                    token = res_data.get("data", {}).get("token")
                    if token:
                        subscription_url = f'{current_url}/api/v1/client/subscribe?token={token}'
                        e_sub.append(subscription_url)
                        print(subscription_url)
                    else:
                        print(f"获取订阅失败 ({current_url}): токен не найден в ответе")
                else:
                    print(f"获取订阅失败 ({current_url}): статус-код {response.status_code}")
            except (requests.RequestException, ValueError, KeyError) as e:
                print(f"获取订阅失败 ({current_url}): {e}")
            i += 1

get_sub_url()
