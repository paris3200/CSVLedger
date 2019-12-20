from csvledger.csvledger import CSVledger


def test_filter_description():
    convertor = CSVledger("tests/sample_config.yml")
    transaction = "ACH Debit BILLPAY TO DUKE ENERGY"
    result = convertor.filter_description(transaction)
    assert result == "BILLPAY TO DUKE ENERGY"


def test_format_debit_transaction():
    convertor = CSVledger("tests/sample_config.yml")
    result = convertor.format_transaction("date", "BP", debit=20.00)
    formatted = "date * BP\n\t\tExpenses:Auto:Gas\t$20.00\n\t\tAssets:Checking\n\n"
    assert result == formatted


def test_format_credit_transaction():
    convertor = CSVledger("tests/sample_config.yml")
    result = convertor.format_transaction("date", "PAY CHECK", credit=20.00)
    formatted = "date * PAY CHECK\n\t\tAssets:Checking\t$20.00\n\t\tIncome\n\n"
    assert result == formatted


def test_format_debit_transaction_with_visa_profile():
    convertor = CSVledger("tests/sample_config.yml", profile="visa")
    result = convertor.format_transaction("date", "BP", debit=20.00)
    formatted = "date * BP\n\t\tExpenses:Auto:Gas\t$20.00\n\t\tLiabilities:Visa\n\n"
    assert result == formatted
