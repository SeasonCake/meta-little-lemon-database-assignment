import openpyxl
import mysql.connector as connector

wb = openpyxl.load_workbook('LittleLemon_Data-.xlsx', data_only=True)
ws = wb['Orders']

connection = connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='YOUR_PASSWORD',
    database='little_lemon'
)
cursor = connection.cursor()

# Drop and recreate tables to fix OrderID duplicate issue
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DROP TABLE IF EXISTS orderdeliverystatus")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS bookings")
cursor.execute("DROP TABLE IF EXISTS menu")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS staff")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

cursor.execute("""
CREATE TABLE customers (
    CustomerID VARCHAR(20) NOT NULL,
    FullName VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    PostalCode VARCHAR(20) NOT NULL,
    CountryCode VARCHAR(5) NOT NULL,
    PRIMARY KEY (CustomerID)
)""")

cursor.execute("""
CREATE TABLE staff (
    StaffID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Salary DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (StaffID)
)""")

cursor.execute("""
CREATE TABLE bookings (
    BookingID INT NOT NULL AUTO_INCREMENT,
    BookingDate DATE NOT NULL,
    TableNumber INT NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    StaffID INT NOT NULL,
    PRIMARY KEY (BookingID),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (StaffID) REFERENCES staff(StaffID)
)""")

cursor.execute("""
CREATE TABLE menu (
    MenuID INT NOT NULL AUTO_INCREMENT,
    CourseName VARCHAR(100) NOT NULL,
    CuisineName VARCHAR(50) NOT NULL,
    StarterName VARCHAR(100) NOT NULL,
    DessertName VARCHAR(100) NOT NULL,
    Drink VARCHAR(100) NOT NULL,
    Sides VARCHAR(100) NOT NULL,
    PRIMARY KEY (MenuID)
)""")

cursor.execute("""
CREATE TABLE orders (
    RowNumber INT NOT NULL,
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    MenuID INT NOT NULL,
    Quantity INT NOT NULL,
    Cost DECIMAL(10,2) NOT NULL,
    Sales DECIMAL(10,2) NOT NULL,
    Discount DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (RowNumber),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (MenuID) REFERENCES menu(MenuID)
)""")

cursor.execute("""
CREATE TABLE orderdeliverystatus (
    DeliveryID INT NOT NULL AUTO_INCREMENT,
    RowNumber INT NOT NULL,
    DeliveryDate DATE NOT NULL,
    DeliveryCost DECIMAL(10,2) NOT NULL,
    DeliveryStatus VARCHAR(50) NOT NULL,
    PRIMARY KEY (DeliveryID),
    FOREIGN KEY (RowNumber) REFERENCES orders(RowNumber)
)""")

connection.commit()
print("Tables recreated.")

print("\nReading Excel data...")
rows = list(ws.iter_rows(min_row=2, values_only=True))
print(f"Total rows: {len(rows)}")

# --- 1. Customers ---
print("\nInserting Customers...")
customers = {}
for row in rows:
    cid = row[4]
    if cid and cid not in customers:
        customers[cid] = (cid, row[5] or '', row[6] or '', row[7] or '', str(row[8]) if row[8] else '', str(row[9]) if row[9] else '')

cursor.executemany(
    "INSERT INTO customers (CustomerID, FullName, City, Country, PostalCode, CountryCode) VALUES (%s, %s, %s, %s, %s, %s)",
    list(customers.values())
)
connection.commit()
print(f"  Inserted {len(customers)} customers")

# --- 2. Menu ---
print("\nInserting Menu...")
menus = {}
menu_counter = 1
for row in rows:
    key = (row[15] or '', row[16] or '', row[17] or '', row[18] or '', row[19] or '', row[20] or '')
    if key not in menus:
        menus[key] = menu_counter
        menu_counter += 1

menu_data = [(mid, k[0], k[1], k[2], k[3], k[4], k[5]) for k, mid in menus.items()]
cursor.executemany(
    "INSERT INTO menu (MenuID, CourseName, CuisineName, StarterName, DessertName, Drink, Sides) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    menu_data
)
connection.commit()
print(f"  Inserted {len(menus)} menu items")

# --- 3. Orders ---
print("\nInserting Orders...")
order_data = []
for row in rows:
    menu_key = (row[15] or '', row[16] or '', row[17] or '', row[18] or '', row[19] or '', row[20] or '')
    mid = menus[menu_key]
    order_date = row[2].strftime('%Y-%m-%d') if row[2] else '2020-01-01'
    cost = float(row[10]) if row[10] else 0
    sales = float(row[11]) if row[11] else 0
    discount = float(row[13]) if row[13] else 0
    quantity = int(row[12]) if row[12] else 0
    order_data.append((int(row[0]), row[1], order_date, row[4], mid, quantity, cost, sales, discount))

batch_size = 5000
for i in range(0, len(order_data), batch_size):
    cursor.executemany(
        "INSERT INTO orders (RowNumber, OrderID, OrderDate, CustomerID, MenuID, Quantity, Cost, Sales, Discount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        order_data[i:i+batch_size]
    )
    connection.commit()
    print(f"  Inserted orders {i+1} to {min(i+batch_size, len(order_data))}")
print(f"  Total: {len(order_data)} orders")

# --- 4. OrderDeliveryStatus ---
print("\nInserting OrderDeliveryStatus...")
delivery_data = []
for row in rows:
    delivery_date = row[3].strftime('%Y-%m-%d') if row[3] else '2020-01-01'
    delivery_cost = float(row[14]) if row[14] else 0
    delivery_data.append((int(row[0]), delivery_date, delivery_cost, 'Delivered'))

for i in range(0, len(delivery_data), batch_size):
    cursor.executemany(
        "INSERT INTO orderdeliverystatus (RowNumber, DeliveryDate, DeliveryCost, DeliveryStatus) VALUES (%s, %s, %s, %s)",
        delivery_data[i:i+batch_size]
    )
    connection.commit()
    print(f"  Inserted deliveries {i+1} to {min(i+batch_size, len(delivery_data))}")
print(f"  Total: {len(delivery_data)} deliveries")

# --- 5. Staff (sample data) ---
print("\nInserting Staff...")
staff_data = [
    (1, 'Adrian Gjonaj', 'Manager', 65000.00),
    (2, 'Mario Gollini', 'Assistant Manager', 50000.00),
    (3, 'Giorgos Dionysius', 'Head Chef', 55000.00),
    (4, 'Fatma Kaya', 'Waiter', 30000.00),
    (5, 'Elena Salvai', 'Waiter', 30000.00),
]
cursor.executemany(
    "INSERT INTO staff (StaffID, Name, Role, Salary) VALUES (%s, %s, %s, %s)",
    staff_data
)
connection.commit()
print(f"  Inserted {len(staff_data)} staff members")

# --- 6. Bookings (sample data) ---
print("\nInserting Bookings...")
sample_customers = list(customers.keys())[:5]
booking_data = [
    (1, '2022-10-10', 5, sample_customers[0], 1),
    (2, '2022-11-12', 3, sample_customers[1], 2),
    (3, '2022-10-11', 2, sample_customers[2], 3),
    (4, '2022-10-13', 2, sample_customers[3], 4),
    (5, '2022-11-14', 7, sample_customers[4], 5),
]
cursor.executemany(
    "INSERT INTO bookings (BookingID, BookingDate, TableNumber, CustomerID, StaffID) VALUES (%s, %s, %s, %s, %s)",
    booking_data
)
connection.commit()
print(f"  Inserted {len(booking_data)} bookings")

cursor.close()
connection.close()
print("\n=== All data imported successfully! ===")
