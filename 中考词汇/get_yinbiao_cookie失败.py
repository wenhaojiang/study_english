import requests

def get_html_request(url, cookies=None, accept=None):
    # 通用的查询模板
    print(f'url: {url}')

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    }
    if accept is not None:
        headers['Accept'] = accept
    if cookies is not None:
        headers['cookie'] = cookies
    response = requests.get(url, headers=headers, allow_redirects=True)
    print(f'response.status_code: {response.status_code}')
    print(f'response.cookies.get_dict(): {response.cookies.get_dict()}')
    # print(f'response.history: {response.history}')
    # print(f'response.text: {response.text}')

    return response

def post_json_request(url, form_data, cookies=None):
    '''
    通用的post请求
    :param url: URL地址
    :param form_data: 编码后的数据
    :return:
    '''
    print(f'url={url}')

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'keep-alive'
    }
    if cookies is not None:
        headers['cookie'] = cookies

    response = requests.post(url, headers=headers, data=form_data)

    response.encoding = 'utf-8'
    print(f'response.status_code: {response.status_code}')
    print(f'response.cookies.get_dict(): {response.cookies.get_dict()}')
    print(f'response.text: {response.text}')

    return response


url = "https://fanyi.baidu.com/?aldtype=85"
rs = get_html_request(url=url)
cookie_dct = rs.cookies.get_dict()
_newcookies = ""
for cookie_key, cookie_value in cookie_dct.items():
    _newcookies += cookie_key + '=' + cookie_value + ';'
print(f"_newcookies: {_newcookies}")

url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
params = {"from": "en", "to": "zh", "query": "walk", "simple_means_flag": "3", "sign": 329224.124217, "token": "ad048234e95c717d499d43f9678fbecd", "domain": "common"}

rs = post_json_request(url=url, form_data=params, cookies=_newcookies)  # 发送请求时，使用data传Parameters参数体
# rs = requests.get(url=url)  # 发送请求时，使用data传Parameters参数体
assert rs.status_code == 200
print(rs.text)

