# coding:utf-8
import requests
from urllib import parse
import argparse
import sys

passer = argparse.ArgumentParser(description='RG_SAM eportal auth')
passer.add_argument('-u', '--username', type=str, required=True, help='RG_SAM eportal web auth username')
passer.add_argument('-p', '--password', type=str, required=True, help='the user password for eportal web auth')
passer.add_argument('-U', '--url', type=str, required=True, help='the url of the eportal auth web server')
group = passer.add_mutually_exclusive_group()
group = passer.add_argument('-q', '--quite', action='store_true', help='just print auth result')
group = passer.add_argument('-v', '--verbose', action='store_true', help='print all auth info')
args = passer.parse_args()


def auth(username, password, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # cookie = "EPORTAL_COOKIE_OPERATORPWD=;EPORTAL_COOKIE_SERVER=;EPORTAL_COOKIE_SERVER_NAME=%E8%AF%B7%E9%80%89%E6%8B%A9%E6%9C%8D%E5%8A%A1;EPORTAL_COOKIE_DOMAIN=;EPORTAL_COOKIE_SAVEPASSWORD=true;EPORTAL_AUTO_LAND=;EPORTAL_USER_GROUP=null;EPORTAL_COOKIE_USERNAME=;EPORTAL_COOKIE_PASSWORD="
    # cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split(";")}
    data = "userId=&password=&service=&queryString=wlanuserip%253Dfb98ca5372f0e5c479250fc7906944c6%2526wlanacname%253D18260f9e92a595cf7b9ea8a87533c165%2526ssid%253Deaa4f48000f25b17215baf6557b1870a%2526nasip%253D3bf45a05888ab2d8978763ee97f3e53a%2526mac%253D63def9e8b5d14061b49d523cd56f5311%2526t%253Dwireless-v2%2526url%253D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false"
    payload = {i.split('=')[0]: i.split('=')[-1] for i in data.split("&")}
    payload['userId'] = parse.quote(username)
    payload['password'] = password
    req = requests.post(url=url + '/eportal/InterFace.do?method=login', headers=headers, data=payload)
    req.encoding = 'utf-8'
    resp = {i.split(":")[0].replace('"', ''): i.split(":")[-1].replace('"', '') for i in req.text[1:-1].split(",")}
    return resp


if __name__ == '__main__':
    if args.url[0:4] != "http":
        print("url example:http://172.16.100.200 or https://172.16.100.200")
        sys.exit(0)
    result = auth(args.username, args.password, args.url)
    if result['message'] == '':
        result['message'] = '认证成功'
    if args.quite:
        print("username:{}\nmessage:{}".format(args.username, result['message']))
    elif args.verbose:
        print(
            "username:{}\nuserindex:{}\nresult:{}\nmessage:{}\nforwordurl:{}\nkeepaliveInterval:{}\nvalidcodeurl:{}\n".format(
                args.username,
                result['userIndex'], result['result'], result['message'], result['forwordurl'],
                result['keepaliveInterval'],
                result['validCodeUrl']))
    else:
        print('userindex:{}\nresult:{}\nmessage:{}\nforwordurl:{}\nkeepaliveInterval:{}\nvalidcodeurl:{}\n'.format(
            result['userIndex'], result['result'], result['message'], result['forwordurl'], result['keepaliveInterval'],
            result['validCodeUrl']))
