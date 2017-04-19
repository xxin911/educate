from . import api
from flask import request, jsonify
from ..zf_educate import sign_in


@api.route('/zf')
def zf():
    if request.method == 'POST':
        url = request.form.get('url')
        number = request.form.get('number')
        password = request.form.get('password')
        txt_sercet_code = request.form.get('code')
        set_cookie = request.form.get('cookie')
        dict = sign_in(url, number, password, txt_sercet_code, set_cookie)
        return jsonify(dict)
    return jsonify({'msg': False})