# from order_ahead import OrderAhead

URL = 'https://www.orderaheadapp.com/sign_in'

import cookielib
import json
import urllib
import urllib2
import credentials

values = {
  'user[email]' : credentials.ORDER_AHEAD_USERNAME,
  'user[password]' : credentials.ORDER_AHEAD_PASSWORD
}

data = urllib.urlencode(values)

cookies = cookielib.CookieJar()
opener = urllib2.build_opener(
  urllib2.HTTPRedirectHandler(),
  urllib2.HTTPHandler(debuglevel=0),
  urllib2.HTTPSHandler(debuglevel=0),
  urllib2.HTTPCookieProcessor(cookies)
)

opener.addheaders = [
  ('Accept', ('application/json, text/javascript, */*; q=0.01')),
  ('User-Agent', ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')),
  ('X-Requested-With', ('XMLHttpRequest'))
]

response = opener.open(URL, data)
parsed_response = json.load(response)

print 'PARSED RESPONSE'
print 'success: ' + str(parsed_response['success'])
print 'token: ' + parsed_response['data']['csrf_token']
