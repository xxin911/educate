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
    radio_button_list1 = '学生'
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

    name_html = soup.select('#xm')
    brithday_html = soup.select('#lbl_csrq')
    department_html = soup.select('#lbl_xy')
    major_html = soup.select('#lbl_zymc')
    class_html = soup.select('#lbl_xzb')
    cid_html = soup.select('#lbl_sfzh')
    grade_html = soup.select('#lbl_dqszj')
    province_html = soup.select('#lbl_lys')
    native_place_html = soup.select('#lbl_jg')
    gender_html = soup.select('#lbl_xb')

    information = {
        'name': name_html[0].string if name_html else None,
        'brithday': brithday_html[0].string if brithday_html else None,
        'department': department_html[0].string if department_html else None,
        'major': major_html[0].string if major_html else None,
        'class': class_html[0].string if class_html else None,
        'cid': cid_html[0].string if cid_html else None,
        'grade': grade_html[0].string if grade_html else None,
        'province': province_html[0].string if province_html else None,
        'native_place': native_place_html[0].string if native_place_html else None,
        'gender': gender_html[0].string if gender_html else None

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