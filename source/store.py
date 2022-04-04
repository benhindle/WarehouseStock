from data_source import DataSource
from operations import Operations
from copy import copy


class Store:
    
    def __init__(self, file_directory):
        self.source = DataSource(file_directory)
        self.operations = Operations()
        self.product_data = self.source.products
        self.updated_orders = {"Fulfilled": [], "Unfulfilled": []}
        self.product_dict = {}

    def process_orders(self, order_ids):  
        for order_id in order_ids:
            order = self.source.get_order(order_id)
            
            # check if orderId input by user exists
            if order != None:
                result = self.check_availablity(order)
                updated_order = result["updated_order"]
                # update order status
                self.updated_orders[order["status"]].append(updated_order)
            else:
                # if orderId dne, return message
                print(f"orderId {order_id} not found")


    def check_availablity(self, order):
        order_list = []
        # loop through products in order
        for item_ordered in order["items"]:
            productId = item_ordered["productId"]

            # use dict to store product for later search - slightly reduces runtime, although as is, still > O(n)
            # dictionary acts somewhat like a cache
            if productId not in self.product_dict:
                # find first occurrence and stop iterating
                product_lookup = next( item for item in self.product_data if item["productId"] == productId )
                # update data store
                self.product_dict[productId] = product_lookup
            
            # copy to temp data struct
            order_list.append(copy(self.product_dict[productId]))
            
            # check inventory
            if order_list[-1]["quantityOnHand"] >= item_ordered["quantity"]:
                order_list[-1]["quantityOnHand"] -= item_ordered["quantity"]
                order["status"] = "Fulfilled"
            else:
                order["status"] = "Unfulfilled"
                # see place_on_backorder() in operations.py.
                # pseudo code not implemented as it was expected to be outside of the scope of the challenge.
                break

        # only if order can be completely fulfilled -> remove items from stock using temp data struct and check for reorder
        if order["status"] == "Fulfilled":
            for prod in order_list:
                self.product_dict[prod["productId"]]["quantityOnHand"] = prod["quantityOnHand"]
                self.reorder_stock(prod)

        return {"updated_order": order, "data": self.product_dict}


    def reorder_stock(self, product):
        # check if stock below threshold, NB. in poduction, this may not be executed after each order fulfillment, rather, at set time period.
            if product["quantityOnHand"] <= product["reorderThreshold"]:
                self.operations.reorder_stock(product)