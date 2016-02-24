import credentials
from order_ahead import OrderAhead

oa = OrderAhead(credentials.ORDER_AHEAD_USERNAME, credentials.ORDER_AHEAD_PASSWORD)


# oa.getCurrentUser()
# oa.getOrdersByStore()
# oa.getWebpage()
# oa.getCurrentOrders()
print 'oa.cart_guid: ' + oa.cart_guid
has_orders = oa.hasCurrentOrders()
print 'has_orders: ' + str(has_orders)

oa.sessionOrder()
# oa.order()

# print 'getUUID: ' + str(getUUID())

# if not oa.hasCurrentOrders():
#   oa.order()
