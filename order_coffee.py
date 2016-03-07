"""Orders Coffee"""
from datetime import datetime
import re
import subprocess
import requests

from order_ahead import OrderAhead
from credentials import IFTTT_MAKER_KEY, ORDER_AHEAD_USERNAME, ORDER_AHEAD_PASSWORD

IFTTT_TRIGGER_URL = 'https://maker.ifttt.com/trigger/order_coffee/with/key/'
IFTTT_MAKER_URL = IFTTT_TRIGGER_URL + IFTTT_MAKER_KEY

def say(say_this):
    subprocess.call(['say', say_this])

def expense_order(order, now):
    data = {
        'value1': order['id'],
        'value2': now.strftime('%m/%d'),
        'value3': float(order['total']) / 100
    }

    request = requests.post(IFTTT_MAKER_URL, data=data)
    if request.status_code is 200:
        say('expense logged')

def order_coffee():
    """orders coffee"""
    now = datetime.today()
    if now.hour > 14:
        message = "it's too late for coffee..."
        say(message)
        print message
        return

    # log in to order ahead
    order_ahead_client = OrderAhead(ORDER_AHEAD_USERNAME, ORDER_AHEAD_PASSWORD)

    if order_ahead_client.has_current_orders():
        message = 'coffee already on order...'
        say(message)
        print message
        return

    print 'ordering coffee...'
    order_response = order_ahead_client.order()
    print order_response['message']

    if order_response['success']:
        order = order_response['order']
        formatted_time = re.sub(r"-08:00", "", order['ready_time'])
        parsed_time = datetime.strptime(formatted_time, "%Y-%m-%dT%H:%M:%S")
        message = "Your coffee will be ready at {0}:{1}{2}".format(
            parsed_time.hour if parsed_time.hour <= 12 else parsed_time.hour - 12,
            parsed_time.minute,
            'AM' if parsed_time.hour < 12 else 'PM'
            )
        say(message)

        # log expense if it is a weekday
        if now.weekday() < 5:
            print 'logging order to spreadsheet...'
            expense_order(order, now)
