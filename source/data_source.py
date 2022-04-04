import json

class DataSource:

    def __init__(self, file_directory):
        with open(file_directory, 'r') as json_data:
            data = json.load(json_data)
            self.products = data["products"]
            self.orders = data["orders"]


    def get_order(self, id):
        filtered_arr = [item for item in self.orders if item["orderId"] == id]
        if len(filtered_arr) > 0:
            return filtered_arr[0]
        else:
            return None