# --- 1. Variables & Data Types ---

# Product A (Laptop)
product_A_name = "Laptop"
product_A_sku = "LT789"
product_A_price = 1200.50
product_A_quantity_in_stock = 15

# Product B (Mouse)
product_B_name = "Wireless Mouse"
product_B_sku = "MS012"
product_B_price = 25.99
product_B_quantity_in_stock = 40

# Product C (Keyboard)
product_C_name = "Mechanical Keyboard"
product_C_sku = "KB345"
product_C_price = 75.00

# --- 3. Casting (for Product C's quantity) ---
initial_qty_str_C = "25"
product_C_quantity_in_stock = int(initial_qty_str_C) # Casting string to integer

print("--- Initial Product Data ---")
print(f"Product A: {product_A_name} (SKU: {product_A_sku}, Price: ${product_A_price:.2f}, Qty: {product_A_quantity_in_stock})")
print(f"Product B: {product_B_name} (SKU: {product_B_sku}, Price: ${product_B_price:.2f}, Qty: {product_B_quantity_in_stock})")
print(f"Product C: {product_C_name} (SKU: {product_C_sku}, Price: ${product_C_price:.2f}, Qty: {product_C_quantity_in_stock})")
print("-" * 30)

# --- 2. Operators ---

print("--- Operator Demonstrations ---")

# Arithmetic Operator: Calculate total value of Product A
product_A_total_value = product_A_price * product_A_quantity_in_stock
print(f"Total value of Product A ({product_A_name}): ${product_A_total_value:.2f}")

# Relational Operator: Is Product B expensive (> $50)?
is_product_B_expensive = product_B_price > 50.00
print(f"Is Product B ({product_B_name}) expensive (> $50)? {is_product_B_expensive}")

# Define a boolean for low stock (for logical operator)
product_C_is_low_stock = product_C_quantity_in_stock < 30 # Assume low stock is below 30

# Logical Operator: Is Product C both 'expensive' (assume > $60) AND 'low in stock'?
is_product_C_expensive = product_C_price > 60.00
is_critical_C = is_product_C_expensive and product_C_is_low_stock
print(f"Is Product C ({product_C_name}) both expensive (> $60) AND low in stock (< 30)? {is_critical_C}")
print("-" * 30)

# --- 4. Strings ---

print("--- String Manipulations ---")

# String Slicing: Extract first three characters of Product A's SKU
sku_prefix_A = product_A_sku[0:3]
print(f"First three characters of Product A SKU ({product_A_sku}): {sku_prefix_A}")

# String Method: Convert Product B's name to uppercase
product_B_name_upper = product_B_name.upper()
print(f"Product B Name in uppercase: {product_B_name_upper}")

# String Concatenation: Create a full description for Product C
full_description_C = product_C_name + " - " + product_C_sku
print(f"Full description for Product C: {full_description_C}")
print("-" * 30)

# --- 5. Booleans ---

print("--- Boolean Variables ---")
product_B_available = True
product_C_on_sale = False
print(f"Is Product B available? {product_B_available}")
print(f"Is Product C on sale? {product_C_on_sale}")
print("-" * 30)

# --- 6. Lists & List Methods ---

print("--- List Manipulations ---")

# Create a single Python list named all_products_data
# Storing each product as a sub-list (more organized)
all_products_data = [
    [product_A_name, product_A_sku, product_A_price, product_A_quantity_in_stock],
    [product_B_name, product_B_sku, product_B_price, product_B_quantity_in_stock],
    [product_C_name, product_C_sku, product_C_price, product_C_quantity_in_stock]
]
print("Initial all_products_data list:")
print(all_products_data)

# Access List Items: Retrieve and print the name of the second product
second_product_name = all_products_data[1][0]
print(f"Name of the second product (index 1, sub-index 0): {second_product_name}")

# Access List Items: Retrieve and print the quantity of the first product
first_product_quantity = all_products_data[0][3]
print(f"Quantity of the first product (index 0, sub-index 3): {first_product_quantity}")

# Change List Items: Directly modify the quantity of the second product (Mouse)
print("\nChanging quantity of Wireless Mouse (Product B) to 55...")
all_products_data[1][3] = 55
print("all_products_data after quantity change:")
print(all_products_data)

# Add List Items: Add data for a fourth new product (Monitor)
print("\nAdding a new product (Monitor)...")
new_product_D = ["Monitor", "MN678", 299.99, 20]
all_products_data.append(new_product_D) # Using append()
print("all_products_data after adding new product:")
print(all_products_data)

# Remove List Items: Remove one product's data (Product A - Laptop)
print("\nRemoving Product A (Laptop)...")
# We'll remove by value of the sub-list directly since we don't have a lookup loop
# If you knew the index, you could use .pop(index)
all_products_data.remove([product_A_name, product_A_sku, product_A_price, product_A_quantity_in_stock])
print("all_products_data after removing Laptop:")
print(all_products_data)


# List Comprehension: Create a new list containing only the SKUs of all products
# This is applied on the current state of all_products_data
print("\nSKUs extracted using List Comprehension:")
all_skus = [product[1] for product in all_products_data]
print(all_skus)


# Copy Lists & Sort Lists: Create a copy and sort it by product name
print("\nProducts sorted by name (copy, original list untouched):")
sorted_products_by_name = all_products_data.copy() # Explicitly create a copy
# Sort using a lambda function to sort by the product name (index 0 of each sub-list)
# The lambda function provides the 'key' for sorting
sorted_products_by_name.sort(key=lambda p: p[0].lower())
print(sorted_products_by_name)
print("Original all_products_data after sort demonstration:")
print(all_products_data) # Verify original is untouched


# Join Lists: Combine a list of bestseller names with current product names
print("\nDemonstrating List Joining (conceptual):")
bestseller_names = ['Tablet', 'Webcam']

# Manually extract current product names for joining demo (no loops)
current_product_names_for_join = [all_products_data[0][0], all_products_data[1][0]] # Mouse, Keyboard, Monitor
if len(all_products_data) > 2: # Check if Monitor is still there after previous operations
    current_product_names_for_join.append(all_products_data[2][0])

combined_names_list = bestseller_names + current_product_names_for_join
print("Combined Bestseller names and Current Product names:")
print(combined_names_list)

print("\n--- End of Demonstration ---")
