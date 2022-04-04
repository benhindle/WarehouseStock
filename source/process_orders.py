from store import Store
import re

FILE_DIRECTORY = "data/data.json"

store = Store(FILE_DIRECTORY)
order_ids = []

# get user input
input_string = input("Please enter a list of order ids to process, in form [id1, id2, id3]:\n")

# clean user input
input_list = input_string.split(",")

for id in input_list:
    order_ids.append(int(re.sub("\D", "", id)))

# process data
store.process_orders(order_ids)

# output result
unfulfilled_orders = set(i['orderId'] for i in store.updated_orders["Unfulfilled"])

if len(unfulfilled_orders) > 0:
    print(f"Unfulfilled orders:\n{unfulfilled_orders}")