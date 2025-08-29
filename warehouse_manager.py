import json
from datetime import date
import os

class Item:
    def __init__(self, name="",quantity=0,price=0.0,location=""):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.location = location
        self.initialize_warehouse()

    def initialize_warehouse(self):
        warehouse_path = "C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json"
        if not os.path.exists(warehouse_path):
            with open(warehouse_path, "w") as file:
                json.dump({}, file)

    def add_item(self):
        try:
            with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
                data = json.load(file)
                name = input("Enter new item's name: ") 
                if name in data:
                    print("Item already exists")
                    return
                else:
                    quantity = int(input("Enter new item's quantity: "))
                    price = float(input("Enter new item's price: "))
                    location = input("Enter new item's location: ")
                    type_choice = input("if perishable item, press 1 else if electronic item, press 2: ")
                    if type_choice == "1":
                        type = "perishable"
                    elif type_choice == "2":
                        type = "electronic"
                    else:
                        print("enter valid number")
                        return

                    if type == "perishable":
                        expiry = date.fromisoformat(input("enter expiry date (YYYY-MM-DD): "))
                        temperature = float(input("enter temperature required: "))
                        isexpired = expiry <= date.today()
                        newItem = {
                            "name": name,
                            "quantity": quantity,
                            "price": price,
                            "location": location,
                            "type": type,
                            "expiry": expiry.isoformat(),
                            "temperature": temperature,
                            "isexpired": isexpired
                        }
                    elif type == "electronic":
                        warranty_start = date.fromisoformat(input("enter warranty start date (YYYY-MM-DD): "))
                        warranty_period = int(input("enter warranty period in days: "))
                        underwarranty = (warranty_start.toordinal() + warranty_period) >= date.today().toordinal()
                        newItem = {
                            "name": name,
                            "quantity": quantity,
                            "price": price,
                            "location": location,
                            "type": type,
                            "warranty_start": warranty_start.isoformat(),
                            "warranty_period": warranty_period,
                            "underwarranty": underwarranty
                        }

                    data[name] = newItem
                    print("After adding:", data)
                    with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "w") as file:
                        json.dump(data, file, indent=4)
        except FileNotFoundError:
            print("Error: warehouse.json not found. Initializing new file.")
            self.initialize_warehouse()
            self.add_item()  # Retry after initialization
        except Exception as e:
            print(f"Error: {e}")
            return

    def remove_item(self,name):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            if name in data:
                del data[name]
                with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "w") as file:
                    json.dump(data, file, indent=4)
            else:
                print("Item not found")

    def update_quantity(self,name,quantity):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            if name in data:
                data[name]['quantity'] = quantity
                with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "w") as file:
                    json.dump(data, file, indent=4)
            else:
                print("Item not found")

    def move_item(self,name,new_location):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            if name in data:
                data[name]['location'] = new_location
                with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "w") as file:
                    json.dump(data, file, indent=4)
            else:
                print("Item not found")

    def stock_check(self):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            for item in data.values():
                print(f"Item: {item['name']}, Quantity: {item['quantity']}")

    def search_item(self,name):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            if name in data:
                item = data[name]
                for key, value in item.items():
                    print(f"{key}: {value}")
            else:
                print("Item not found")

    def check_expiry(self):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            for item in data.values():
                if item['type'] == 'perishable':
                    expiry_date = date.fromisoformat(item['expiry'])
                    if expiry_date < date.today():
                        print(f"Item {item['name']} has expired.")
                    else:
                        print(f"Item {item['name']} will expire in {(expiry_date - date.today()).days} days.")

    def check_warranty(self):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            for item in data.values():
                if item['type'] == 'electronic':
                    warranty_start = date.fromisoformat(item['warranty_start'])
                    warranty_period = item['warranty_period']
                    if (warranty_start.toordinal() + warranty_period) < date.today().toordinal():
                        print(f"Item {item['name']}'s warranty has expired.")
                    else:
                        print(f"Item {item['name']} will be out of warranty in {(warranty_start.toordinal() + warranty_period) - date.today().toordinal()} days.")

    def extend_warranty(self,name,days):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data=json.load(file)
            if name in data:
                if data[name]['type']=='electronic':
                    data[name]['warranty_period']+=days
                    with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "w") as file:
                        json.dump(data, file, indent=4)
                else:
                    print("Item is not electronic")

    def generate_report(self):
        with open("C:/Users/Harshvardhan Bajpai/Desktop/warehouse.json", "r") as file:
            data = json.load(file)
            total_items = len(data)
            total_value = sum(item['quantity'] * item['price'] for item in data.values())
            perishable_count = sum(1 for item in data.values() if item['type'] == 'perishable')
            electronic_count = sum(1 for item in data.values() if item['type'] == 'electronic')

            print(f"Total number of items: {total_items}")
            print(f"Total value of items: {total_value}")
            print(f"Number of perishable items: {perishable_count}")
            print(f"Number of electronic items: {electronic_count}")

def main():
    wms = Item("",0,0.0,"")
    while True:
        print("Warehouse Management System")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Update Quantity")
        print("4. Move Item")
        print("5. Stock Check")
        print("6. Search Item")
        print("7. Check Expiry")
        print("8. Check Warranty")
        print("9. Extend Warranty")
        print("10. Generate Report")
        print("11. Exit")
        
        input_choice = int(input("Enter your choice (1-11): "))
        
        if input_choice == 1:
            print()
            wms.add_item()
        elif input_choice == 2:
            name = input("Enter item name to remove: ")
            print()
            wms.remove_item(name)
        elif input_choice == 3:
            print()
            name = input("Enter item name to update quantity: ")
            quantity = int(input("Enter new quantity: "))
            wms.update_quantity(name, quantity)
        elif input_choice == 4:
            print()
            name = input("Enter item name to move: ")
            new_location = input("Enter new location: ")
            wms.move_item(name, new_location)
        elif input_choice == 5:
            print()
            wms.stock_check()
        elif input_choice == 6:
            print()
            name = input("Enter item name to search: ")
            wms.search_item(name)
        elif input_choice == 7:
            print()
            wms.check_expiry()
        elif input_choice == 8:
            print()
            wms.check_warranty()
        elif input_choice == 9:
            print() 
            name = input("Enter item name to extend warranty: ")
            days = int(input("Enter number of days to extend: "))
            wms.extend_warranty(name, days)
        elif input_choice == 10:
            print()
            wms.generate_report()
        elif input_choice == 11:
            print()
            print("Exiting system...")
            break
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()

