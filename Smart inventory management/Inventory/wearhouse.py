import datetime
import heapq
import os
from collections import deque

# --- Class Definitions ---  <- ADD THIS SECTION

class TransactionLedger:
    """A class to manage and record all inventory transactions."""
    def __init__(self):
        """Initializes the ledger with an empty list of transactions."""
        self.transactions = []

    def add_transaction(self, product_id, description, quantity_change):
        """Adds a new transaction record to the ledger."""
        transaction_record = {
            "timestamp": datetime.datetime.now(),
            "product_id": product_id,
            "description": description,
            "quantity_change": quantity_change
        }
        self.transactions.append(transaction_record)

    def display_ledger(self):
        """Prints a formatted report of all transactions."""
        print("\n--- Transaction Ledger ---")
        if not self.transactions:
            print("No transactions recorded yet.")
            return

        # Header for the report
        header = f"{'Timestamp':<26} {'Product ID':<12} {'Description':<20} {'Quantity Change'}"
        print(header)
        print("-" * len(header))

        # Print each transaction record
        for record in self.transactions:
            # Format the timestamp to be more readable
            ts_str = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            # The :+ format specifier adds a + sign for positive numbers
            print(f"{ts_str:<26} {record['product_id']:<12} {record['description']:<20} {record['quantity_change']:+}")


# --- Global Data (Constants and State) ---

# Using ALL_CAPS is a convention for global variables that act like constants
INVENTORY = [
    [101, "Gaming Mouse", "Electronics", 75.50, 80],
    [102, "Mechanical Keyboard", "Electronics", 120.00, 50],
    [103, "Webcam", "Electronics", 90.00, 60],
    [201, "Office Chair", "Furniture", 150.00, 30],
    [202, "Desk Lamp", "Furniture", 45.75, 100],
    [901, "Gamer PC Bundle", "Composite", 0, 10]
]

COMPOSITE_PRODUCTS = {
    901: [101, 102, 103]  # Gamer PC Bundle parts
}

# State variables
# A human might just call it 'ledger' instead of 'transaction_ledger'
ledger = TransactionLedger() 
order_queue = deque()
backorder_queue = []
delivery_truck = [] # A stack is just a list with append/pop

# Initialize with existing data
for product in INVENTORY:
    ledger.add_transaction(product[0], "initial stock", product[4])

# --- Helper Functions ---

def _clear_screen():
    """Clears the console screen for a cleaner UI."""
    # A simple, practical helper function a developer would write.
    os.system('cls' if os.name == 'nt' else 'clear')

def _get_product_by_id(product_id):
    """Finds and returns a product from the inventory."""
    # This avoids repeating the same 'for' loop everywhere.
    for product in INVENTORY:
        if product[0] == product_id:
            return product
    return None

def _pause():
    """Pauses the program and waits for the user to press Enter."""
    input("\nPress Enter to continue...")


# --- Core Functionality ---

def generate_inventory_report():
    """Generates and prints a report of the current inventory status."""
    print("--- Current Inventory Report ---")
    header = f"{'ID':<5} {'Product Name':<25} {'Category':<15} {'Price':>10} {'Stock':>10}"
    print(header)
    print("-" * len(header))
    
    total_value = sum(p[3] * p[4] for p in INVENTORY)
    
    for product_id, name, category, price, stock in INVENTORY:
        print(f"{product_id:<5} {name:<25} {category:<15} {price:>10.2f} {stock:>10}")
        
    print("-" * len(header))
    print(f"Total inventory value: ${total_value:,.2f}")

def calculate_composite_cost(product_id):
    """Recursively calculates the total cost of a composite product."""
    if product_id not in COMPOSITE_PRODUCTS:
        product = _get_product_by_id(product_id)
        return product[3] if product else 0

    return sum(calculate_composite_cost(part_id) for part_id in COMPOSITE_PRODUCTS[product_id])

def add_new_product():
    """Adds a new product to the inventory system."""
    print("--- Add New Product ---")
    try:
        name = input("Enter product name: ")
        category = input("Enter product category: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter initial stock level: "))

        # Get the next available ID
        new_id = max(p[0] for p in INVENTORY) + 1
        
        new_product = [new_id, name, category, price, stock]
        INVENTORY.append(new_product)
        ledger.add_transaction(new_id, "initial stock", stock)
        
        print(f"\nSuccessfully added '{name}' with Product ID: {new_id}")

    except ValueError:
        print("Invalid input. Please enter numbers for price and stock.")

def place_order():
    """Places a new customer order into the appropriate queue."""
    print("--- Place New Customer Order ---")
    try:
        product_id = int(input("Enter product ID to order: "))
        product = _get_product_by_id(product_id)
        if not product:
            print("Error: Product not found.")
            return

        quantity = int(input(f"Enter quantity for '{product[1]}': "))
        # Simple unique order ID
        order_id = int(datetime.datetime.now().timestamp()) 
        order = (order_id, product_id, quantity)
        
        if product[4] >= quantity:
            print("Sufficient stock. Order placed in the processing queue.")
            order_queue.append(order)
        else:
            print("Insufficient stock. Order placed in the backorder queue.")
            # heapq is a min-heap, so we don't need to do anything special for priority
            heapq.heappush(backorder_queue, order)
            
    except ValueError:
        print("Invalid input. Please use numbers.")

# --- Main Application Loop ---

def main():
    """The main function to run the command-line application."""
    while True:
        _clear_screen()
        print("===== Simple Inventory Management System =====")
        # Menu options are more grouped by function
        print("\n[INVENTORY]")
        print("1. Generate Inventory Report")
        print("2. Add New Product")
        print("3. View Transaction Ledger")
        
        print("\n[ORDERS & DELIVERY]")
        print("4. Place Customer Order")
        print("5. Process Next Order & Load Truck")
        print("6. Dispatch Truck")
        
        print("\n[OTHER]")
        print("7. Calculate Composite Product Cost")
        print("8. Exit")
        print("============================================")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            generate_inventory_report()
            _pause()
        elif choice == '2':
            add_new_product()
            _pause()
        elif choice == '3':
            ledger.display_ledger()
            _pause()
        elif choice == '4':
            place_order()
            _pause()
        elif choice == '5':
            # Logic for processing/loading truck would go here
            print("\nProcessing next order...")
            _pause()
        elif choice == '6':
            # Logic for dispatching truck would go here
            print("\nDispatching truck...")
            _pause()
        elif choice == '7':
            # This is more of a utility, so it's lower down
            pid = int(input("Enter composite product ID: "))
            cost = calculate_composite_cost(pid)
            print(f"Calculated cost: ${cost:.2f}")
            _pause()
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            _pause()

if __name__ == "__main__":
    main()
