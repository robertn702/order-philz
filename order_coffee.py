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

  if not oa.hasCurrentOrders():
    if now.hour < 15:
      print 'ordering coffee...'
      order_response = oa.order()
      print order_response['message']

      # do not log expense if it is the weekend
      if order_response['success'] && now.weekday() < 5:
        print 'logging order to spreadsheet...'
        order = order_response['order']
        expense_order(order)
    else:
      print "it's too late for coffee..."
  else:
    print 'coffee already on order...'
