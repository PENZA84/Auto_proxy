# coding=utf-8
import base64
import requests
import re
import time
import os
import threading
from tqdm import tqdm
import random, string
import datetime
from time import sleep
import chardet

# 试用机场链接
home_urls = (
    'https://xn--30rs3bu7r87f.com',
    'https://seeworld.pro',          # 5T   永久
    'https://fastestcloud.xyz',      # 2G   1天
    'https://www.ckcloud.xyz',       # 1G   1天
)
# 文件路径
update_path = "./sub/"
# 所有的clash订阅链接
end_list_clash = []
# 所有的v2ray订阅链接
end_list_v2ray = []
# 所有的节点明文信息
end_bas64 = []
# 获得格式化后的链接
new_list = []
# 永久订阅
e_sub = ['https://sub.pmsub.me/base64','https://www.prop.cf/?name=paimon&client=base64','https://raw.githubusercontent.com/yaney01/Yaney01/main/temporary','https://sub.pmsub.me/base64','https://raw.githubusercontent.com/hkaa0/permalink/main/proxy/V2ray','https://sub.sharecentre.online/sub','https://raw.githubusercontent.com/freefq/free/master/v2','https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub','https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/free','https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub']
# 频道
urls = ["https://t.me/s/freeVPNjd","https://t.me/s/wxdy666","https://t.me/s/nice16688","https://t.me/s/go4sharing","https://t.me/s/helloworld_1024","https://t.me/s/dingyue_Center","https://t.me/s/ZDYZ2"]
# 线程池
threads = []
# 机场链接
plane_sub = ['https://www.prop.cf/?name=paimon&client=base64']
# 机场试用链接
try_sub = []
# 获取频道订阅的个数
sub_n = -5
# 试用节点明文
end_try = []

# 获取群组聊天中的HTTP链接
def get_channel_http(url):
    headers = {
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://t.me/s/wbnet',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        response = requests.post(url, headers=headers, timeout=12)
        pattren = re.compile(r'"https+:[^\s]*"')
        return pattren.findall(response.text)
    except requests.RequestException:
        return []

# 对bs64解密
def jiemi_base64(data):  
    try:
        data = data.strip()
        # Автоматическое исправление отсутствующего паддинга Base64
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
            
        decoded_bytes = base64.b64decode(data)
        detected = chardet.detect(decoded_bytes)
        encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
        return decoded_bytes.decode(encoding, errors='ignore')
    except Exception:
        return ""

# 判读是否为订阅链接
def get_content(url):
    url_lst = get_channel_http(url)
    for i in url_lst:
        result = i.replace("\\", "").replace('"', "")
        if result not in new_list:
            if len(result) > 8 and "t" not in result[8]:
                if len(result) > 2 and "p" not in result[-2]:
                    new_list.append(result)
                    
    try:
        new_list_down = new_list[sub_n::]
    except Exception:
        new_list_down = new_list[len(new_list) * 2 // 3::]
        
    for o in new_list_down:
        try:
            res = requests.get(o, timeout=10)
            if not res.text:
                continue
            # 判断是否为clash
            if 'proxies:' in res.text:
                end_list_clash.append(o)
            else:
                # 判断是否为v2
                peoxy = jiemi_base64(res.text)
                if peoxy:
                    end_list_v2ray.append(o)
                    end_bas64.extend(peoxy.splitlines())
        except Exception:
            pass
    return end_bas64

# 写入文件
def write_document():
    if not e_sub and not try_sub and not end_bas64:
        print("订阅为空请检查！")
        return

    # 永久订阅
    random.shuffle(e_sub)
    for e in e_sub:
        try:
            res = requests.get(e, timeout=10)
            proxys = jiemi_base64(res.text)
            if proxys:
                end_bas64.extend(proxys.splitlines())
        except Exception:
            print(e, "永久订阅出现错误❌跳过")
    print('永久订阅更新完毕')
    
    # 试用订阅
    random.shuffle(try_sub)
    for t in try_sub:
        try:
            res = requests.get(t, timeout=10)
            proxys = jiemi_base64(res.text)
            if proxys:
                end_try.extend(proxys.splitlines())
        except Exception as er:
            print(t, "试用订阅出现错误❌跳过", er)
    print('试用订阅更新完毕', try_sub)
    
    # 永久订阅去重
    end_bas64_A = list(set(end_bas64))
    print("去重完毕！！去除", len(end_bas64) - len(end_bas64_A), "个重复节点")
    
    # 去除多余换行符
    bas64 = '\n'.join(end_bas64_A).replace('\n\n', "\n")
    bas64_try = '\n'.join(end_try).replace('\n\n', "\n")
    
    # 获取时间，给文档命名用
    t_local = time.localtime()
    date = time.strftime('%y%m', t_local)
    date_day = time.strftime('%y%m%d', t_local)
    
    # 创建文件路径
    try:
        os.makedirs(f'{update_path}{date}', exist_ok=True)
    except Exception:
        pass
        
    txt_dir = update_path + date + '/' + date_day + '.txt'
    
    # Safe file write using context manager
    with open(txt_dir, 'w', encoding='utf-8') as file:
        file.write(bas64)
        
    # 减少获取的个数
    r = 1
    length = len(end_bas64_A)  # 总长
    m = 8  # 切分成多少份
    step = int(length / m) + 1  # 每份的长度
    
    for i in range(0, length, step):
        print("起", i, "始", i + step)
        zhengli = '\n'.join(end_bas64_A[i: i + step]).replace('\n\n', "\n")
        obj = base64.b64encode(zhengli.encode())
        plaintext_result = obj.decode()
        
        with open("Long_term_subscription" + str(r), 'w', encoding='utf-8') as file_L:
            file_L.write(plaintext_result)
        r += 1
        
    # 写入总长期订阅
    obj = base64.b64encode(bas64.encode())
    plaintext_result = obj.decode()
    with open("Long_term_subscription_num", 'w', encoding='utf-8') as file_L:
        file_L.write(plaintext_result)
        
    # 写入试用订阅
    obj_try = base64.b64encode(bas64_try.encode())
    plaintext_result_try = obj_try.decode()
    with open("Long_term_subscription_try", 'w', encoding='utf-8') as file_L_try:
        file_L_try.write(plaintext_result_try)
        
    # 写入README
    lines = []
    if os.path.exists("README.md"):
        with open("README.md", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
    TimeDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for index in range(len(lines)):
        try:
            if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_num`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {length}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription1`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription4`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription5`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription6`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription7`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {step}`\n')
            if lines[index] == f'`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription8`\n':
                lines.pop(index + 1)
                lines.insert(index + 1, f'`Total number of merge nodes: {length - step * 7}`\n')
            if lines[index] == '`https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3.yaml`\n':
                lines.pop(index + 4)
                lines.pop(index + 4)
                lines.insert(index + 4, f'Updata：`{TimeDate}`\n')
                lines.insert(index + 4, f'### Try the number of high-speed subscriptions: `{len(try_sub)}`\n')
            if lines[index] == '>Trial subscription：\n':
                lines.pop(index)
                lines.pop(index)
        except Exception:
            pass
            
    # 写入试用订阅
    for index in range(len(lines)):
        try:
            if lines[index] == '## ✨Star count\n':
                n_offset = 5
                for TrySub in try_sub:
                    lines.insert(index - n_offset, f'\n>Trial subscription：\n`{TrySub}`\n')
                    n_offset += 3
        except Exception:
            print("写入试用出错")
            
    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(''.join(lines))
        
    print("合并完成✅")
    try:
        with open(txt_dir, 'r', encoding='utf-8') as f:
            numbers = sum(1 for _ in f)
        print("共获取到", numbers, "节点")
    except Exception:
        print("出现错误！")
    return

# 获取clash订阅
def get_yaml():
    print("开始获取clash订阅")
    urls = [
        "https://api.dler.io/sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_try&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true",
        "https://api.dler.io/sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription2&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true", 
        "https://api.dler.io/sub?target=clash&url=https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription3&insert=false&config=https://raw.githubusercontent.com/w1770946466/fetchProxy/main/config/provider/rxconfig.ini&emoji=true"
    ]
    n = 1
    for i in urls:
        try:
            response = requests.get(i, timeout=15)
            response.raise_for_status()
            with open("Long_term_subscription" + str(n) + ".yaml", 'w', encoding='utf-8') as file_L:
                file_L.write(response.text)
            n += 1
        except Exception as e:
            print(f"获取Clash订阅 {i} 失败: {e}")
    print("clash订阅获取完成！")

# 获取机场试用订阅
def get_sub_url():
    V2B_REG_REL_URL = '/api/v1/passport/auth/register'
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
            if current_url in ('https://xn--4gqu8thxjfje.com', 'https://seeworld.pro', 'https://www.jwckk.top', 'https://vvtestatiantian.top'):
                try:
                    fan_res = requests.post(f'{current_url}/api/v1/passport/auth/register', data=form_data, headers=header, timeout=10)
                    if fan_res.status_code == 200:
                        auth_data = fan_res.json().get("data", {}).get("auth_data")
                        if auth_data:
                            fan_header = {
                                'Origin': current_url,
                                'Authorization': ''.join(auth_data),
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Connection': 'keep-alive',
                                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                                'Referer': current_url,
                            }
                            fan_data = {
                                'period': 'onetime_price',
                                'plan_id': '1',
                            }
                            fan_res_n = requests.post(f'{current_url}/api/v1/user/order/save', headers=fan_header, data=fan_data, timeout=10)
                            trade_no = fan_res_n.json().get("data")
                            if trade_no:
                                fan_data_n = {'trade_no': trade_no}
                                requests.post(f'{current_url}/api/v1/user/order/checkout', data=fan_data_n, headers=fan_header, timeout=10)
                                token = fan_res.json().get("data", {}).get("token")
                                if token:
                                    subscription_url = f'{current_url}/api/v1/client/subscribe?token={token}'
                                    try_sub.append(subscription_url)
                                    print("add:" + subscription_url)
                except Exception as result:
                    print(result)
                    break
            else:
                try:
                    response = requests.post(current_url + V2B_REG_REL_URL, data=form_data, headers=header, timeout=10)
                    if response.status_code == 200:
                        token = response.json().get("data", {}).get("token")
                        if token:
                            subscription_url = f'{current_url}/api/v1/client/subscribe?token={token}'
                            try_sub.append(subscription_url)
                            print("add:" + subscription_url)
                except Exception as e:
                    print("获取订阅失败", e)
            i += 1

# ========== 抓取 kkzui.com 的节点 ==========  
def get_kkzui():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://kkzui.com/jd?orderby=modified", headers=headers, timeout=10)
        article_url = re.search(r'class="media-content" href="(.*?)"', res.text).groups()[0]
        res = requests.get(article_url, headers=headers, timeout=10)
        sub_url = re.search(r'<strong>这是v2订阅地址：(.*?)</strong>', res.text).groups()[0]
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取kkzui.com完成！")
    except Exception as e:
        print("获取kkzui.com失败！", e)
        
# ========== 抓取 cfmem.com 的节点 ==========
def get_cfmem():
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://www.cfmem.com/search/label/free", headers=headers, timeout=10)
        article_url = re.search(r"https?://www\.cfmem\.com/\d{4}/\d{2}/\S+v2rayclash-vpn.html", res.text).group()
        res = requests.get(article_url, headers=headers, timeout=10)
        sub_url = re.search(r'>v2ray订阅链接&#65306;(.*?)</span>', res.text).groups()[0]
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取cfmem.com完成！")
    except Exception as e:
        print("获取cfmem.com失败！", e)

# ========== 抓取 v2rayshare.com 的节点 ==========
def get_v2rayshare():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://v2rayshare.com/", headers=headers, timeout=10)
        article_url = re.search(r'https://v2rayshare.com/p/\d+\.html', res.text).group()
        res = requests.get(article_url, headers=headers, timeout=10)
        sub_url = re.search(r'<p>https://v2rayshare.com/wp-content/uploads/(.*?)</p>', res.text).groups()[0]
        sub_url = 'https://v2rayshare.com/wp-content/uploads/' + sub_url
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取v2rayshare.com完成！")
    except Exception as e:
        print("获取v2rayshare.com失败！", e)

# ========== 抓取 nodefree.org 的节点 ==========
def get_nodefree():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"}
        res = requests.get("https://nodefree.org/", headers=headers, timeout=10)
        article_url = re.search(r'https://nodefree.org/p/\d+\.html', res.text).group()
        res = requests.get(article_url, headers=headers, timeout=10)
        sub_url = re.search(r'<p>https://nodefree.org/dy/(.*?)</p>', res.text).groups()[0]
        sub_url = 'https://nodefree.org/dy/' + sub_url
        try_sub.append(sub_url)
        e_sub.append(sub_url)
        print("获取nodefree.org完成！")
    except Exception as e:
        print("获取nodefree.org失败！", e)
        
    
if __name__ == '__main__':
    print("========== 开始获取机场订阅链接 ==========")
    get_sub_url()
    print("========== 开始获取网站订阅链接 ==========")
    get_kkzui()
    get_cfmem()
    get_v2rayshare()
    get_nodefree()
    print("========== 开始获取频道订阅链接 ==========")
    for url in urls:
        thread = threading.Thread(target=get_content, args=(url,))
        thread.start()
        threads.append(thread)
        
    # 等待线程结束
    for t in tqdm(threads):
        t.join()
        
    print("========== 准备写入订阅 ==========")
    write_document()
    get_yaml()
    print("========== 写入完成任务结束 ==========")
