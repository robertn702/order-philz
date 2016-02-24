PAST_ORDERS = 'https://www.orderaheadapp.com/api/v1.0.10/users/orders/by_store?per=30&shallow=1&web_serializer=1'
import credentials
from order_ahead import OrderAhead

oa = OrderAhead(credentials.ORDER_AHEAD_USERNAME, credentials.ORDER_AHEAD_PASSWORD)

print 'oa.cart_guid: ' + oa.cart_guid

# oa.getCurrentUser()
# oa.getOrdersByStore()
# oa.getWebApp()
# oa.getCurrentOrders()
has_orders = oa.hasCurrentOrders()
print 'has_orders: ' + str(has_orders)

oa.sessionOrder()
# oa.order()

# print 'getUUID: ' + str(getUUID())
