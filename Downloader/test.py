import requests
import json

def post2port(target):
    data = {
        'total': 3,
        'crawl_url_list': {
            'tt3208026.jpg':'https://pic1.zhimg.com/v2-2a1b6b73f933f692668a7be5cf08db5e_1200x500.jpg',
            'tt3208012.jpg':'https://pic1.zhimg.com/v2-2a1b6b73f933f692668a7be5cf08db5e_1200x500.jpg',
            'tt3208000.jpg':'https://pic1.zhimg.com/v2-2a1b6b73f933f692668a7be5cf08db5e_1200x500.jpg'
            },
    }
    ## headers中添加上content-type这个参数，指定为json格式
    headers = {'Content-Type': 'application/json'}
    ## post的时候，将data字典形式的参数用json包转换成json格式。
    response = requests.post(url=target, headers=headers, data=json.dumps(data))
    print(response)
if __name__ == "__main__":
    url = "http://127.0.0.1:7060/crawl"
    post2port(url)