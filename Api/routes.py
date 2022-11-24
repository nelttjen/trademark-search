import requests
import pyquery
from flask import jsonify, request
from flask_restful import abort, Resource
from Site.update_cookie import session, update_cookie


def generate_link(endpoint, key, query, array, rnum='', anum='', appl=''):
    payload = {
        'ajax': 'tmsearch',
        'act': 'trademarkSearch',
        'session_key': key,
        'name': query,
        'rnum': rnum,
        'anum': anum,
        'appl': appl,
        'extended': 0,
        'getstr': ''
    }
    endpoint += '?'
    args = []
    for key, val in payload.items():
        args.append(f'{key}={val}')
    for val in array:
        args.append(f'mktu[]={val}')
    return endpoint + '&'.join(args)


class TrademarkSearch(Resource):
    def post(self):
        req_data = request.get_json()
        if not req_data.get('query'):
            return abort(400, message='query parameter undefined')
        query = req_data.get('query')
        key = session.cookies.get('f_session_key')

        if req_data.get('mktu_array'):
            raw = req_data.get('mktu_array')
            try:
                mktu_array = list(map(int, raw.split(',')))
            except:
                return abort(400, message='mktu parameter malformed')
        else:
            mktu_array = []

        rnum = req_data.get('rnum') or ''
        anum = req_data.get('anum') or ''
        appl = req_data.get('appl') or ''

        endpoint = 'https://onlinepatent.ru/'

        link = generate_link(endpoint, key, query, mktu_array, rnum, anum, appl)
        response = session.get(link)
        if response.text == 'Ajax access denied.':
            key = update_cookie()
            link = generate_link(endpoint, key, query, mktu_array, rnum, anum, appl)
            response = session.get(link)

        json_obj = response.json()

        if json_obj['error']:
            return abort(400, message='api answer is wrong')

        trademark_count = json_obj['count']
        trademark_items = json_obj['data']
        trademark_objects = []
        max_word = 0.0
        if trademark_count > 0:
            if mktu_array:
                _iter = trademark_items.values()
            else:
                _iter = trademark_items
            for item in _iter:
                _id = item.get('id')
                img = item.get('img')
                index = item.get('index')
                name = item.get('name')
                mktu = item.get('mktu')
                trademark_objects.append({
                    'id': _id,
                    'index': index,
                    'name': name,
                    'img': img,
                    'mktu': mktu
                })
                if query.lower() in name.lower():
                    max_word = max(max_word, len(query) / len(name))
        return jsonify({
            'message': 'OK',
            'total_found': trademark_count,
            'word_percent_found': float('%.2f' % max_word),
            'query_items': trademark_objects,
        })


class TrademarkInfo(Resource):
    def post(self):
        
        req_data = request.get_json()
        if not req_data.get('index'):
            return abort(400, message='index parameter undefined')
        url = f'https://onlinepatent.ru/trademarks/{req_data.get("index")}/'
        response = requests.get(url)
        if response.status_code != 200:
            return abort(response.status_code, message='fail')
        try:
            query = pyquery.PyQuery(response.text)
            item0, item1 = list(query.find('.tm-about__data-item').items())

            subtitle = query.find('span.uni-about__subtitle').text()
            main_title = query.find('h1.main-title').text()

            try:
                priority = list(item0.find('.uni-about__data-text').items())[0].text()
            except:
                priority = 'нет данных'
                
            try:
                member = list(item0.find('.uni-about__data-text').items())[1].text()
            except:
                member = 'нет данных'
                
            try:
                address = list(item0.find('.uni-about__data-text').items())[2].text()
            except:
                address = 'нет данных'
                
            try:
                unsecured_elements = list(item0.find('.uni-about__data-text').items())[3].text()
            except:
                unsecured_elements = 'нет данных'
                
            try:
                send_date = list(item1.find('.uni-about__data-text').items())[0].text()
            except:
                send_date = 'нет данных'
                
            try:
                register_date = list(item1.find('.uni-about__data-text').items())[1].text()
            except:
                register_date = 'нет данных'
                
            try:
                publish_date = list(item1.find('.uni-about__data-text').items())[2].text()
            except:
                publish_date = 'нет данных'
                
            try:
                expired_date = list(item1.find('.uni-about__data-text').items())[3].text()
            except:
                expired_date = 'нет данных'
                
            try:
                image = query.find('span.tm-about__square-pic').attr('style').replace("background-image: url('", '')[:-2]
            except:
                image = None
            mktu = []
            for item in query.find('.mktu-classes__item').items():
                curr_mktu = {
                    'mktu_number': item.text(),
                    'mktu_data': item.attr('data-text'),
                }
                mktu.append(curr_mktu)

            item_json = {
                "index": int(req_data.get('index')),
                "main_title": main_title,
                'subtitle': subtitle,
                'priority': priority,
                'member': member,
                'address': address,
                'unsecured_elements': unsecured_elements,
                'send_date': send_date,
                'register_date': register_date,
                'publish_date': publish_date,
                'expired_date': expired_date,
                'mktu': mktu,
                'image': image,
            }

            return jsonify({'message': 'ok', 'item': item_json})
        except Exception as e:
            print(e)
            return abort(500, message='server error')
