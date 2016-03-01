"""ORDER AHEAD"""
from Cookie import SimpleCookie
import json
import random
import re
import requests

URLS = {
    'current_orders' : 'https://www.orderaheadapp.com/api/v1.0.10/users/orders/current',
    'login': 'https://www.orderaheadapp.com/sign_in',
    'by_store': 'https://www.orderaheadapp.com/api/v1.0.10/users/orders/by_store',
    'current_user': 'https://www.orderaheadapp.com/current_user',
    'order': 'https://www.orderaheadapp.com/orders?client_name=computer&api_version=1.0.10',
    'session-order': 'https://www.orderaheadapp.com/session-order',
    'store-menu': 'https://www.orderaheadapp.com/api/v1.0.10/stores/1z3ofd/menu'
}

DEFAULT_HEADERS = {
    'Accept': 'application/json, text/javascript, */* q=0.01',
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_11_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def cookie_to_dict(cookie_str):
    cookie = SimpleCookie()
    cookie.load(cookie_str)
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value

    return cookies

def is_json(request):
    return 'application/json' in request.headers['Content-Type']

def get_uuid():
    seed_uuid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    def generate_uuid(e_val):
        match_val = e_val.group(0)
        t_val = int(round(float(0|16) * random.random()))
        request = t_val if match_val == 'x' else 8|3&t_val
        return format(request, 'x')

    return re.sub(r"[xy]", lambda x: generate_uuid(x), seed_uuid)


class OrderAhead(object):
    """Order Ahead Client"""
    token = None
    cart_guid = None
    session = requests.Session()

    def __init__(self, username, password):
        self.session.headers.update(DEFAULT_HEADERS)
        self.login(username, password)
        self.login(username, password)
        self.cart_guid = get_uuid()

    def login(self, username, password):
        """Logs user in"""
        data = {
            'user[email]': username,
            'user[password]': password
        }

        request = self.session.post(URLS['login'], data=data, headers=self.session.headers)
        parsed_response = request.json()
        token = parsed_response['data']['csrf_token']
        self.session.headers.update({
            'X-CSRF-Token': token,
            'Cookie': '_orderahead_session=' + request.cookies['_orderahead_session']
        })

    def get_current_user(self):
        """returns current user object"""
        request = self.session.get(URLS['current_user'])
        if is_json(request):
            return request.json()

    def get_current_orders(self):
        """returns current orders object"""
        request = self.session.get(URLS['current_orders'])
        if is_json(request):
            return request.json()['orders']

    def has_current_orders(self):
        """returns boolean whether user has a current order"""
        return len(self.get_current_orders()) > 0

    def get_orders_by_store(self):
        """returns past orders by store"""
        request = self.session.get(URLS['by_store'])
        if is_json(request):
            return request.json()['data']
        else:
            print 'ERROR, response must be JSON. Type: ' + request.headers['Content-Type']

    def get_store_menu(self):
        """returns store menu"""
        request = self.session.get(URLS['store-menu'])
        if request.status_code is 200:
            if is_json(request):
                return request.json()
        else:
            print 'failed to get store menu'

    # def sessionOrder(self):
    #     self.session_orderequest = {
    #         "order": {
    #             "store_id": "1z3ofd",
    #             "bag_items_attributes": [
    #                 {
    #                   "menu_item_id": "23dgi0k7",
    #                   "special_instructions": "",
    #                   "quantity": 1,
    #                   "selected_menu_item_options": "{\"67322\":[418458],\"67325\":[418464],\"67326\":[418470],\"67327\":[418475],\"67328\":[418482],\"67329\":[418485]}",
    #                   "user_name": "Robert Niimi",
    #                   "user_id": "21fgk8rp"
    #                 }
    #             ],
    #             "preparation_type": 0,
    #             "cart_guid": str(self.cart_guid),
    #             "tier_delivery_fees": True,
    #             "unwaivable_delivery_fees": True,
    #             "store_slug": "philz-coffee-san-mateo--san-mateo-ca"
    #         }
    #     }

    #     headers = s.headers.copy()
    #     headers.update({'Content-Type': 'application/json'})

    #     request = s.put(URLS['session-order'], data=json.dumps(self.session_order), headers=headers)
    #     print 'Session Order Status Code: ' + str(r.status_code)

    def order(self):
        """places an order"""
        store_menu = self.get_store_menu()
        prep_duration = store_menu['default_prep_duration'] + store_menu['additional_prep_duration']

        order_obj = {
            "order": {
                "store_id": "1z3ofd",
                "bag_items_attributes": [
                    {
                        "menu_item_id": "23dgi0k7",
                        "special_instructions": "",
                        "quantity": 1,
                        "selected_menu_item_options": "{\"67322\":[418458],\"67325\":[418464],\"67326\":[418470],\"67327\":[418475],\"67328\":[418482],\"67329\":[418485]}",
                        "user_name": "Robert Niimi",
                        "user_id": "21fgk8rp"
                    }
                ],
                "cart_guid": str(self.cart_guid),
                "payment_card_id": "11pq9xfj",
                "preparation_type": 0,
                "selected_wait_time": prep_duration,
                "store_slug": "philz-coffee-san-mateo--san-mateo-ca",
                "tier_delivery_fees": True,
                "unwaivable_delivery_fees": True
            }
        }

        headers = self.session.headers.copy()
        headers.update({'Content-Type': 'application/json'})

        request = self.session.post(URLS['order'], data=json.dumps(order_obj), headers=headers)

        if request.status_code == 500:
            print 'Order Failed'

        if is_json(request):
            return request.json()
        else:
            print request.text
