from datetime import datetime
from order_ahead import OrderAhead
import credentials
import requests


def order_coffee():
  # log in to order ahead
  oa = OrderAhead(credentials.ORDER_AHEAD_USERNAME, credentials.ORDER_AHEAD_PASSWORD)

  if not oa.hasCurrentOrders():
    print 'ordering coffee...'

    order = oa.order()

    data = {
      'value1': order['id'],
      'value2': datetime.today().strftime('%m/%d'),
      'value3': float(order['total'])/100
    }

    r = requests.post('https://maker.ifttt.com/trigger/order_coffee/with/key/d5KrJ5q56csJvG-J3Misj7', data=sample_data)
    print 'r.status_code: ' + str(r.status_code)

  else
    print 'coffee already on order...'
