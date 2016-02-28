# import credentials
# import cookielib
import requests
import json
import uuid
import random
import re
from Cookie import SimpleCookie
s = requests.Session()

URLS = {
  'web_app': 'https://www.orderaheadapp.com',
  'current_orders' : 'https://www.orderaheadapp.com/api/v1.0.10/users/orders/current',
  'login': 'https://www.orderaheadapp.com/sign_in',
  'by_store': 'https://www.orderaheadapp.com/api/v1.0.10/users/orders/by_store?per=30&shallow=1&web_serializer=1',
  'current_user': 'https://www.orderaheadapp.com/current_user',
  'order': 'https://www.orderaheadapp.com/orders?client_name=computer&api_version=1.0.10',
  'session-order': 'https://www.orderaheadapp.com/session-order',
  'store-menu': 'https://www.orderaheadapp.com/api/v1.0.10/stores/1z3ofd/menu'
}

default_headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest'
}

s.headers.update(default_headers)

def cookie_to_dict(cookieStr):
  cookie = SimpleCookie()
  cookie.load(cookieStr)
  cookies = {}
  for key, morsel in cookie.items():
      cookies[key] = morsel.value

  return cookies

def is_json(r):
  return 'application/json' in r.headers['Content-Type']

class OrderAhead():
  token = None
  cart_guid = None

  def __init__(self, username, password):
    self.login(username, password);
    self.login(username, password);
    self.cart_guid = self.getUUID();

  def getUUID(self):
    seed_uuid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    def generateUUID(e):
      match_val = e.group(0)
      t = int(round(float(0|16) * random.random()))
      r = t if "x" == match_val else 8|3&t
      return format(r, 'x')

    return re.sub(r"[xy]", lambda x: generateUUID(x), seed_uuid)

  def login(self, username, password):
    data = {
      'user[email]' : username,
      'user[password]' : password
    }

    r = s.post(URLS['login'], data=data, headers=s.headers);
    parsed_response = r.json()
    token = parsed_response['data']['csrf_token']
    s.headers.update({
      'X-CSRF-Token': token,
      'Cookie': '_orderahead_session=' + r.cookies['_orderahead_session']
    })

  def getWebpage(self):
    r = requests.get(URLS['web_app'])
    return r.text

  def getCurrentUser(self):
    r = s.get(URLS['current_user'])
    if is_json(r):
      return r.json()

  def getCurrentOrders(self):
    r = s.get(URLS['current_orders'])
    if is_json(r):
      return r.json()['orders']

  def hasCurrentOrders(self):
    return len(self.getCurrentOrders()) > 0;

  def getOrdersByStore(self):
    r = s.get(URLS['by_store'])
    if is_json(r):
      return r.json()['data']
    else:
      print 'ERROR, response must be JSON. Type: ' + r.headers['Content-Type']

  def getStoreMenu(self):
    r = s.get(URLS['store-menu'])
    if r.status_code is 200:
      if is_json(r):
        return r.json()
    else:
      print 'failed to get store menu'

  def sessionOrder(self):
    self.session_order = {
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
        "preparation_type": 0,
        "cart_guid": str(self.cart_guid),
        "tier_delivery_fees": True,
        "unwaivable_delivery_fees": True,
        "store_slug": "philz-coffee-san-mateo--san-mateo-ca"
      }
    }

    headers = s.headers.copy()
    headers.update({'Content-Type': 'application/json'})

    r = s.put(URLS['session-order'], data=json.dumps(self.session_order), headers=headers)
    print 'Session Order Status Code: ' + str(r.status_code)

  def order(self):
    store_menu = self.getStoreMenu()
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

    headers = s.headers.copy()
    headers.update({'Content-Type': 'application/json'})

    r = s.post(URLS['order'], data=json.dumps(order_obj), headers=headers)

    if r.status_code == 500:
      print 'Order Failed'

    if is_json(r):
      return r.json()
    else:
      print r.text


