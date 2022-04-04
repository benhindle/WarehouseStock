class Operations:

    def __init__(self):
        self.stock_already_ordered = {} # may not be sufficient for production, see further explanation below. Just used as quick check here to prevent double ordering.
        # self.ordered_stock = {
            # "backorder_stock": 0, #backordered for existing order in system
            #  "ordered_excess": 0 # result of fulfilling order with qty in excess of reorderAmount || for stockOnHand
        # }

    def reorder_stock(self, product):
        if product["productId"] not in self.stock_already_ordered:
            print(f"reordering stock for item productId: {product['productId']}")
            self.stock_already_ordered[product["productId"]] = True
        # Need to be careful here not to place multiple orders of stock where subsequent orders are
        #  fulfilled with quantityOnHand met whilst being below reorderThreshold (e.g. if [1122,1123] entered).
        #  This is where tracking using the above "ordered_stock" or similar structures may be required,
        #  including using a backorder system if in production.
        
    # def place_on_backorder(self):
    # 1.0 check if there is enough order_excess to fulfill order upon arrival of stock
    #   - if true -> do 1.1
    #   - if false -> do 1.2
    # 
    # 1.1 remove order qty from "ordered_excess" and add to "backorder_stock"
    # 1.2 Assume "reorderAmount" is a minimum order qty set by supplier. After minimum "reorderAmount" amount,
    #       smaller increments can be made (ie if reorderAmount=10, orders can be placed for 10+n).
    #   - place order for max(reorderAmount, order qty) -> call it order_placed
    #   - add order qty to "backorder_stock"
    #   - check if order_placed > order qty
    #       - if true -> do 1.2.1
    # 1.2.1 add (order_placed - order qty) to "ordered_excess"
    # 
    # Check if reorderThreshold is gt ordered_excess
    #  - if true -> 1.2.2
    #  - if false -> return
    # 
    # 1.2.2 add difference to order (reorderThreshold - order_excess)
    # 
    # NB additional functionality will be required to keep track of allocating "backorder_stock".
    #  This may require storage in separate part of database or adding fields to existing product objects,
    #  depending on department requirements. Date of order (by customer) and lead time from supplier would also
    #  be taken into consideration.