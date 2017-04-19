#_*_coding:utf8_*_
import requests
from bs4 import BeautifulSoup
import re

login_url = 'http://jwxt.gcu.edu.cn/default2.aspx'
code_url = 'http://jwxt.gcu.edu.cn/CheckCode.aspx'


def get_cookies(set_cookie):

    session_id = re.search('ASP.NET_SessionId=(.*?);', set_cookie)
    array_cookie = re.search('array_cookie=(.*?);', set_cookie)

    if session_id and array_cookie:
        cookies = {
            'ASP.NET_SessionId': session_id.group(1),
            'array_cookie': array_cookie.group(1),
        }
    if array_cookie is None:
        cookies = {
            'ASP.NET_SessionId': session_id.group(1),
        }
    return cookies


def get_view_state(url, cookies):
    login_response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(login_response.text, 'html.parser')
    __VIEWSTATE = soup.find(attrs={"name": '__VIEWSTATE'})['value']
    return __VIEWSTATE


def post_data(url, number, password, txt_secret_code, cookies):
    radio_button_list1 = '\321\247\311\372'
    __VIEWSTATE = get_view_state(url, cookies)
    data = {
        '__VIEWSTATE': __VIEWSTATE,
        'txtUserName': number,
        'TextBox2': password,
        'txtSecretCode': txt_secret_code,
        'RadioButtonList1': radio_button_list1,
        'hidPdrs': '',
        'hidsc': '',
        'Button1': '',
        'lbLanguage': ''
    }
    sign_in_response = requests.post('{}default2.aspx'.format(url), data=data, cookies=cookies)
    return sign_in_response


def get_info(url, number, cookies):
    info_url = '{}xsgrxx.aspx?xh={}'.format(url, number)

    info_body = requests.get(info_url, headers={'Referer': url}
                             , cookies=cookies).text

    soup = BeautifulSoup(info_body, 'html.parser')

    information = {
        'name': soup.select('#xm')[0].string,
        'brithday': soup.select('#lbl_csrq')[0].string,
        'department': soup.select('#lbl_xy')[0].string,
        'major': soup.select('#lbl_zymc')[0].string,
        'class': soup.select('#lbl_xzb')[0].string,
        'cid': soup.select('#lbl_sfzh')[0].string,
        'grade': soup.select('#lbl_dqszj')[0].string,
        'province': soup.select('#lbl_lys')[0].string,
        'native_place': soup.select('#lbl_jg')[0].string,
        'gender': soup.select('#lbl_xb')[0].string

    }
    return information

def sign_in(url, number, password, txt_secret_code, set_cookie):
    cookies = get_cookies(set_cookie)
    response = post_data(url, number, password, txt_secret_code, cookies)
    if response.history and response.history[0].status_code == 302:
        information = get_info(url, number, cookies)
        return dict(status=True, information=information)
    else:
        return dict(status=False)