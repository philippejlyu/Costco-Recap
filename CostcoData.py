import json
from typing import *
import os
import pandas as pd

def create_item_set():
    # Iterate through ./receipts/*.json
    directory_path = "./Receipts/"
    item_numbers = set()
    items = {}
    try:
        json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

        for file_name in json_files:
            file_path = os.path.join(directory_path, file_name)

            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    item_array = data['data']['receiptsWithCounts']['receipts'][0]['itemArray']
                    for item in item_array:
                        if item['itemNumber'] not in item_numbers:
                            item_numbers.add(item['itemNumber'])
                            items[item['itemNumber']] = item
                        
            except json.JSONDecodeError:
                print(f"Error: The file '{file_name}' contains invalid JSON.")
    except:
        print("error")
    
    try:
        with open("item_database.json", 'w') as file:
            json.dump(items, file, indent=4)
    except:
        print("error")


def process_data():
    files = ['./Costco_Jan_June.json', './Costco_July_Dec_2024.json']
    receipts = []
    items_purchased = {}
    not_found_items = []
    item_database = None
    with open('item_database.json', 'r') as file:
        item_database = json.load(file)
        file.close()

    if item_database is None:
        return

    for filename in files:
        with open(filename, 'r') as file:
            data = json.load(file)
            receipts.extend(data['data']['receiptsWithCounts']['receipts'])
            for receipt in data['data']['receiptsWithCounts']['receipts']:
                items = receipt['itemArray']
                for item in items:
                    item_number = item['itemNumber']
                    if item_number in items_purchased:
                        items_purchased[item_number]['numPurchased'] += 1
                    else:
                        if item_number in item_database:
                            items_purchased[item_number] = {"name1": item_database[item_number]['itemDescription01'], 
                                                            "name2": item_database[item_number]['itemDescription02'],
                                                            "price": item_database[item_number]['amount'],
                                                            "numPurchased": 1}
                        else:
                            items_purchased[item_number] = {"itemNumber": item_number,
                                                            "numPurchased": 1}
                            not_found_items.append({"itemNumber": item_number,
                                                    "date": receipt['transactionDateTime']})
    
    costco_df = pd.DataFrame(receipts)
    item_df = pd.DataFrame(items_purchased)

    warehouse_counts = costco_df["warehouseName"].value_counts()
    print("Warehouses visited: ")
    print(warehouse_counts)

    total_spent = costco_df['total'].sum()
    print("Total spent at costco:")
    print(total_spent)

    rotisserie_chicken = items_purchased['347937']

    print("You bought this many rotisserie chickens")
    print(rotisserie_chicken['numPurchased'])

    sorted_items = sorted(items_purchased.items(), key=lambda x: x[1]['numPurchased'], reverse=True)
    top_items = sorted_items[:10]

    print("Your top purchased items are: ")
    for item in top_items:
        print(items_purchased[item[0]])

    




if __name__ == '__main__':
    create_item_set()
    process_data()