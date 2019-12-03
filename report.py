import csv


def filter_description(row):
    result = row
    remove_text = [
        "Point of Sale",
        "L340",
        "DATE",
        "Debit",
        "WINSTON-SALE",
        "WINSTON SALE",
        "MOUNT AIRY",
        "MT AIRY",
        "KING",
        "PINNACLE",
    ]
    for text in remove_text:
        result = result.replace(text, "")
    result = result.strip()
    return result


def categorize_transaction(description):
    categories = {
        "LOWE'S FOODS": "Expenses:Food:Grocery",
        "ALDI": "Expenses:Food:Grocery",
        "LIDL": "Expenses:Food:Grocery",
        "FOUR BRO": "Expenses:Auto:Gas",
        "SHEETZ": "Expenses:Auto:Gas",
        "DAIRI-O": "Expenses:Food:Dining",
        "MCDONALD'S": "Expenses:Food:Dining",
        "STARBUCKS": "Expenses:Food:Dining",
        "BOJANGLES": "Expenses:Food:Dining",
        "PLAZA DEL SOL": "Expenses:Food:Dining",
    }
    for store, category in categories.items():
        if store in description:
            return category


# Open file
with open("transaction.csv", "r", newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    credit = 0
    debit = 0

    # Skip Header Row
    next(csv_reader)

    for row in csv_reader:
        try:
            credit += float(row[3])
        except ValueError:
            pass

        try:
            debit += float(row[4])
        except ValueError:
            pass

        # print(f"{row[0]} \t {filter_description(row[2])} \t {row[3]} \t {row[4]}")
        description = filter_description(row[2])
        print(f"{row[0]} \t {description}")
        print(f"\t \t {categorize_transaction(description)}")
        print("\t \t Assets:Checking \n")
        print("\t \t Assets:Checking \n")

    print(f"Credit: +{format(credit, '.2f')}")
    print(f"Debit: -{format(debit, '.2f')}")
    print(f"Change: {format(credit-debit, '.2f')}")
