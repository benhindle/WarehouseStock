# class Store:

# process orders (main func called)
    # Loop through orderIds
        # check if orderId input by user exists
        # call func to check for stock availability
        # update order status

        # if orderId dne, return message


# check stock availability for order
    # loop through products in order
        # try to use some kind of cache to reduce runtime for subsequent searches

        # check inventory

    # condition - only if all items present in inventory -> fulfil order and remove items from stock
        # reorder stock if below threshold -> operations