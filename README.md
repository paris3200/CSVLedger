[![Build Status](https://travis-ci.org/paris3200/CSVLedger.svg?branch=master)](https://travis-ci.org/paris3200/CSVLedger)[![codecov](https://codecov.io/gh/paris3200/CSVLedger/branch/master/graph/badge.svg)](https://codecov.io/gh/paris3200/CSVLedger)

# CSVLedger
Convert CSV fanancial transactions to ledger journal


CSVLedger converts a CVS file downloaded from a fanancial instution into a
ledgercli journal file.  Currently it is under development and not ready for
production use.  However, if you're ok with editing some Python code to set
some account variables it will work.

```
csvledger --help
Usage: csvledger [OPTIONS]
    CSVledger taks the input of a CSV file of financial transactions, strips excessive
    data from the transactions and then converts the transactions to ledger-cli
    format.

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

    git clone https://github.com/paris3200/CSVLedger.git
    cd csvledger

Install the requirements using Pip.

    pip install -r requirements-dev.txt

Finally install CSVLedger.

    python setup.py install


## Release History

* 0.3.0
    * Minor refactoring
* 0.2.0
    * Added support for YAML config
* 0.1.2
    * Travis CI added
* 0.1.1
    * Restructed Project
* 0.1.0
    * Work in progress

## Meta

Jason Paris – paris3200@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/paris3200/CSVLedger](https://github.com/paris3200/CSVLedger)

## Contributing

1. Fork it (<https://github.com/paris3200/CSVLedger/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
