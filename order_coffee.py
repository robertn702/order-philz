"""Orders Coffee"""
from datetime import datetime
import requests

from order_ahead import OrderAhead
from credentials import IFTTT_MAKER_KEY, ORDER_AHEAD_USERNAME, ORDER_AHEAD_PASSWORD

IFTTT_TRIGGER_URL = 'https://maker.ifttt.com/trigger/order_coffee/with/key/'
IFTTT_MAKER_URL = IFTTT_TRIGGER_URL + IFTTT_MAKER_KEY

def expense_order(order, now):
    data = {
        'value1': order['id'],
        'value2': now.strftime('%m/%d'),
        'value3': float(order['total'])/100
    }

    request = requests.post(IFTTT_MAKER_URL, data=data)
    print 'log to spreadsheet status: ' + str(request.status_code)

def order_coffee():
    """orders coffee"""
    now = datetime.today()
    if now.hour > 14:
        print "it's too late for coffee..."
        return

    # log in to order ahead
    order_ahead_client = OrderAhead(ORDER_AHEAD_USERNAME, ORDER_AHEAD_PASSWORD)

    if order_ahead_client.has_current_orders():
        print 'coffee already on order...'
        return

    print 'ordering coffee...'
    order_response = order_ahead_client.order()
    print order_response['message']

    # log expense if it is a weekday
    if order_response['success'] and now.weekday() < 5:
        print 'logging order to spreadsheet...'
        order = order_response['order']
        expense_order(order, now)
