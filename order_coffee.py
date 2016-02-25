import credentials
from order_ahead import OrderAhead

oa = OrderAhead(credentials.ORDER_AHEAD_USERNAME, credentials.ORDER_AHEAD_PASSWORD)


# oa.getCurrentUser()
# oa.getOrdersByStore()
# oa.getWebpage()
# oa.getCurrentOrders()

oa.sessionOrder()
oa.sessionOrder()

# print 'has_orders: ' + str(has_orders)
if not oa.hasCurrentOrders():
  print 'ordering coffee...'
  oa.order()
