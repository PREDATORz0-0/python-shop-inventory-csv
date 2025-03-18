import csv
class Product:
    def __init__(self, product_id, product_name, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.price = float(price)
        self.quantity = int(quantity)
    def __str__(self):
        return f"{self.product_id} | {self.product_name} | {self.price} | {self.quantity}"
    def update_quantity(self, quantity):
        self.quantity -= quantity
    def update_price(self, price):
        self.price = price
class Inventory:
    def __init__(self):
        self.products = []
        self.load_inventory()
    def load_inventory(self):
        try:
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.products.append(Product(*row))
        except FileNotFoundError:
            pass
    def add_product(self, product):
        self.products.append(product)
        self.save_inventory()
    def save_inventory(self):
        with open('inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["product_id", "product_name", "price", "quantity"])
            for product in self.products:
                writer.writerow([product.product_id, product.product_name, product.price, product.quantity])
    def update_product(self, product_id, quantity):
        for product in self.products:
            if product.product_id == product_id:
                product.update_quantity(quantity)
                self.save_inventory()
                return True
        return False
    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    def display_inventory(self):
        headers = ["Product ID", "Product Name", "Price", "Quantity"]
        print(f"{headers[0]:<15}{headers[1]:<20}{headers[2]:<10}{headers[3]:<10}")
        for product in self.products:
            print(f"{product.product_id:<15}{product.product_name:<20}{product.price:<10}{product.quantity:<10}")
class Sale:
    def __init__(self, sale_id):
        self.sale_id = sale_id
        self.products_sold = []
        self.total_price = 0
    def add_product_to_sale(self, product, quantity):
        self.products_sold.append((product, quantity))
        self.total_price += product.price * quantity
    def calculate_total(self):
        return self.total_price
class SalesManager:
    def __init__(self):
        self.sales = []
        self.load_sales()
    def load_sales(self):
        try:
            with open('sales.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    sale_id, product_id, product_name, quantity_sold, total_price = row
                    sale = Sale(sale_id)
                    sale.add_product_to_sale(Product(product_id, product_name, "", ""), int(quantity_sold))
                    self.sales.append(sale)
        except FileNotFoundError:
            pass
    def record_sale(self, sale):
        self.sales.append(sale)
        self.save_sales()
    def save_sales(self):
        with open('sales.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["sale_id", "product_id", "product_name", "quantity_sold", "total_price"])
            for sale in self.sales:
                for product, quantity in sale.products_sold:
                    writer.writerow([sale.sale_id, product.product_id, product.product_name, quantity, sale.calculate_total()])
    def display_sales_report(self):
        headers = ["Sale ID", "Product ID", "Product Name", "Quantity Sold", "Total Price"]
        print(f"{headers[0]:<10}{headers[1]:<15}{headers[2]:<20}{headers[3]:<15}{headers[4]:<10}")
        for sale in self.sales:
            for product, quantity in sale.products_sold:
                print(f"{sale.sale_id:<10}{product.product_id:<15}{product.product_name:<20}{quantity:<15}{sale.calculate_total():<10}")
class ShopSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.sales_manager = SalesManager()
    def display_menu(self):
        print("\n1. View Inventory")
        print("2. Add Product to Inventory")
        print("3. Update Product in Inventory")
        print("4. Make a Sale")
        print("5. View Sales Report")
        print("6. Exit")
    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.inventory.display_inventory()
            elif choice == "2":
                self.add_product_to_inventory()
            elif choice == "3":
                self.update_product_in_inventory()
            elif choice == "4":
                self.make_sale()
            elif choice == "5":
                self.sales_manager.display_sales_report()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")
    def add_product_to_inventory(self):
        product_id = input("Enter product ID: ")
        product_name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        new_product = Product(product_id, product_name, price, quantity)
        self.inventory.add_product(new_product)
        print("Product added to inventory.")
    def update_product_in_inventory(self):
        product_id = input("Enter product ID to update: ")
        quantity = int(input("Enter quantity to update: "))
        if self.inventory.update_product(product_id, quantity):
            print("Product updated.")
        else:
            print("Product not found.")
    def make_sale(self):
        sale_id = input("Enter sale ID: ")
        sale = Sale(sale_id)
        while True:
            product_id = input("Enter product ID to sell (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            quantity = int(input("Enter quantity: "))
            product = self.inventory.get_product_by_id(product_id)
            if product and product.quantity >= quantity:
                sale.add_product_to_sale(product, quantity)
                self.inventory.update_product(product_id, quantity)
                print(f"Added {quantity} of {product.product_name} to sale.")
            else:
                print("Not enough stock or invalid product ID.")
        self.sales_manager.record_sale(sale)
        print(f"Sale recorded with total price: {sale.calculate_total()}")
if __name__ == "__main__":
    shop = ShopSystem()
    shop.handle_user_input()
