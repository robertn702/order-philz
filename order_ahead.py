# import credentials
# import cookielib
import requests
from Cookie import SimpleCookie
s = requests.Session()

URLS = {
  'login': 'https://www.orderaheadapp.com/sign_in',
  'by_store': 'https://www.orderaheadapp.com/api/v1.0.10/users/orders/by_store?per=30&shallow=1&web_serializer=1',
  'current_user': 'https://www.orderaheadapp.com/current_user'
}

default_headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
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

  def __init__(self, username, password):
    self.login(username, password);
    self.login(username, password);

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

  def getCurrentUser(self):
    r = s.get(URLS['current_user'])
    if is_json(r):
      parsed_response = r.json()
      print '@getCurrentUser RESPONSE: ' + r.text

  def getOrdersByStore(self):
    r = s.get(URLS['by_store'])
    if is_json(r):
      parsed_response = r.json()
      print '@getOrdersByStore RESPONSE: ' + r.text
    else:
      print 'XXXXX ERROR, response must be JSON. Type: ' + r.headers['Content-Type']

