# CSVledger
Convert CSV fanancial transactions to ledger journal


CSVLedger converts a CVS file downloaded from a fanancial instution into a
ledgercli journal file.  Currently it is under development and not ready for
production use.  However, if you're ok with editing some Python code to set
some account variables it will work.

```
 csvledger --help
Usage: csvledger [OPTIONS]

  This script coverts CSV files downloaded from a financial instution to
  ledger entries.  Each entry is categorized using the business name to
  determine the spending category.

Options:
  --config PATH       path to config file
  -i, --csvfile PATH  csv file to be converted
  --check             prints all transaction without an expense/income
                      category.
  --total             prints sum of all credit and debit transactions
  --convert           prints transactions in ledger format
  --help              Show this message and exit.
```

## Installation


### Development setup

It is recommended that you install CSVLedger in a virtual environment to
prevent conflicts with other python packages.  First create the virtual
environment, activate it, and follow the install directions below.

To install CSVLedger begin by cloning the repo and changing to the directory. ::

    git clone https://github.com/paris3200/csvledger.git
    cd csvledger

Install the requirements using Pip. ::

    pip install -r requirements-dev.txt

Finally install CSVLedger. ::

    python setup.py install


## Release History

* 0.1.0
    * Work in progress

## Meta

Jason Paris – paris3200@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/paris3200/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/paris3200/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
