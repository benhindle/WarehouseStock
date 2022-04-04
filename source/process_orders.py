from store import Store
from reports import Report
import re

FILE_DIRECTORY = "data/data.json"

store = Store(FILE_DIRECTORY)
report = Report()
order_ids = []

# -- Data processing -- #

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

# -- Generate reports -- #
req_stock_report = input("Would you like a report of fulfilled/unfulfilled orders? (please enter Y/N):\n")
if req_stock_report.lower() == "y":
    report.generate_fulfilled_report(store.updated_orders)

req_stock_report = input("Would you like a current stock report? (please enter Y/N):\n")
if req_stock_report.lower() == "y":
    report.generate_stock_report(store.product_data)