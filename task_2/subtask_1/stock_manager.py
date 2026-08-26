def load_stock():
    try:
        with open("stock.txt", "r") as file:
            stock = {}

            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 2:
                    raise ValueError

                name = parts[0].strip().lower()
                amount = int(parts[1].strip())

                if name == "" or amount < 0:
                    raise ValueError

                stock[name] = amount

            return stock

    except FileNotFoundError:
        print("stock.txt was not found.")
        return {}

    except (ValueError, IndexError):
        print("stock.txt is corrupted.")
        return {}

    except Exception:
        print("An error occurred while reading stock.txt.")
        return {}


def show_stock(stock):
    if len(stock) == 0:
        print("Stock is empty.")
        return

    for i, (name, amount) in enumerate(stock.items(), 1):
        print(f"{i}. {name}: {amount}")


def get_stock_item(stock, allow_new):
    while True:
        user_input = input("Enter the stock name or ID: ").strip()

        if user_input == "":
            print("Input cannot be empty.")
            continue

        if user_input.isdigit():
            item_id = int(user_input)

            if 1 <= item_id <= len(stock):
                return list(stock.keys())[item_id - 1]

            print("Invalid ID.")
            continue

        name = user_input.lower()

        if name in stock:
            return name

        if allow_new:
            return name

        print("This stock does not exist.")


def get_amount():
    while True:
        value = input("Enter the amount: ").strip()

        try:
            amount = int(value)

            if amount > 0:
                return amount

            print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid whole number.")


def add_stock(stock):
    show_stock(stock)

    name = get_stock_item(stock, True)

    amount = get_amount()

    if name in stock:
        stock[name] += amount
    else:
        stock[name] = amount

    print("Stock updated successfully.")


def remove_stock(stock):
    if len(stock) == 0:
        print("Stock is empty.")
        return

    show_stock(stock)

    name = get_stock_item(stock, False)

    while True:
        amount = get_amount()

        if amount <= stock[name]:
            stock[name] -= amount
            print("Stock updated successfully.")
            break

        print(f"You cannot remove more than {stock[name]}.")


def save_stock(stock):
    try:
        with open("stock.txt", "w") as file:
            for name, amount in stock.items():
                file.write(f"{name},{amount}\n")

    except Exception:
        print("An error occurred while saving.")


stock = load_stock()

while True:
    print("\n1. Enter 1 to add stock")
    print("2. Enter 2 to remove stock")
    print("3. Enter 3 to show stock's contents")
    print("4. Enter 4 to exit the program")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_stock(stock)
        save_stock(stock)

    elif choice == "2":
        remove_stock(stock)
        save_stock(stock)

    elif choice == "3":
        show_stock(stock)

    elif choice == "4":
        save_stock(stock)
        print("Program ended.")
        break

    else:
        print("Please enter only 1, 2, 3, or 4.")