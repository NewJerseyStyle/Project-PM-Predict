import requests
import re

def get_proxy_list(test_url=None):
    response = requests.get("https://www.sslproxies.org/")

    proxy_ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', response.text)  #「\d+」代表數字一個位數以上

    valid_ips = []
    for ip in tqdm(proxy_ips):
        try:
            url = 'https://ip.seeip.org/jsonip?'
            if test_url:
                url = test_url
            result = requests.get(url,
                 proxies={'http': ip, 'https': ip},
                 timeout=5)
            if test_url is None or '<title>Google</title>' in result:
                valid_ips.append(ip)
        except:
            pass

    return valid_ips
