import requests
import json

API_KEY = "gKMOfVu47gp3BMMUJb8EPpfG"
SECRET_KEY = "1G5RdeXf9RdIjj6bzeF4A1udqT8jTEPl"

def main(body):
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": body,
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    

    response = requests.request("POST", url, 
                                headers=headers, 
                                data=payload)
    
    print(response.text)
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main([{"role": "user", "content":"我需要和房东签订什么合同？"}])
