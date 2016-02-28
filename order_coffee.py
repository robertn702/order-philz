from datetime import datetime
from order_ahead import OrderAhead
import credentials
import requests

IFTTT_MAKER_URL = 'https://maker.ifttt.com/trigger/order_coffee/with/key/' + credentials.IFTTT_MAKER_KEY

def expense_order(order):
  data = {
    'value1': order['id'],
    'value2': now.strftime('%m/%d'),
    'value3': float(order['total'])/100
  }

  r = requests.post(IFTTT_MAKER_URL, data=data)
  print 'log to spreadsheet status: ' + str(r.status_code)

def order_coffee():
  # log in to order ahead
  oa = OrderAhead(credentials.ORDER_AHEAD_USERNAME, credentials.ORDER_AHEAD_PASSWORD)
  now = datetime.today()

  if oa.hasCurrentOrders():
    print 'coffee already on order...'
    return

  if now.hour > 14:
    print "it's too late for coffee..."
    return

  print 'ordering coffee...'
  order_response = oa.order()
  print order_response['message']

  # log expense if it is a weekday
  if order_response['success'] and now.weekday() < 5:
    print 'logging order to spreadsheet...'
    order = order_response['order']
    expense_order(order)
