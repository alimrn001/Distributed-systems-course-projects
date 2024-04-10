user_order_items = []

while True:
    input_line = input("Enter elements separated by spaces: ")
    input_elements = input_line.split()

    if input_elements:
        user_order_items.extend(input_elements)
        break

    print("Please enter at least one element.")

print("Array:", user_order_items)
