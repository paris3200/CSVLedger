from csvledger.csvledger import CSVledger


def test_filter_description():
    convertor = CSVledger("tests/sample_config.yml")
    transaction = "ACH Debit BILLPAY TO DUKE ENERGY"
    result = convertor.filter_description(transaction)
    assert result == "BILLPAY TO DUKE ENERGY"


def test_format_debit_transaction():
    convertor = CSVledger("tests/sample_config.yml")
    result = convertor.format_transaction("date", "BP", debit=20.00)
    formatted = (
        "date * BP \n \t \t Expenses:Auto:Gas \t $20.00 \n \t \t Assets:Checking \n"
    )
    assert result == formatted.strip()


def test_format_credit_transaction():
    convertor = CSVledger("tests/sample_config.yml")
    result = convertor.format_transaction("date", "PAY CHECK", credit=20.00)
    formatted = "date * PAY CHECK \n \t \t Assets:Checking \t $20.00 \n \t \t Income \n"
    assert result == formatted.strip()
