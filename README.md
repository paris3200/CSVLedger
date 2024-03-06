 [![codecov](https://codecov.io/gh/paris3200/CSVLedger/branch/master/graph/badge.svg)](https://codecov.io/gh/paris3200/CSVLedger) [![Documentation Status](https://readthedocs.org/projects/csvledger/badge/?version=latest)](https://csvledger.readthedocs.io/en/latest/?badge=latest)


# CSVLedger
Convert CSV financial transactions to ledger journal

Turn this:

    Process Dates,Check Number,Description,Credit Amount,Debit Amount
    8/5/2019,,Point of Sale Debit  DATE 08-03 CHICK-FIL-A,,13.28
    8/5/2019,,Point of Sale Debit  DATE 08-03 WAL-MART,,69.98
    8/5/2019,,Point of Sale Debit  DATE 08-03 LIDL,,107.91

Into:

    2019/08/05 * CHICK-FIL-A
		Expenses:Food:Dining	$13.28
		Assets:Checking

    2019/08/05 * WAL-MART
		Expenses:Food:Grocery	$69.98
		Assets:Checking

    2019/08/05 * LIDL
		Expenses:Food:Grocery	$107.91
		Assets:Checking



See [Quickstart Guide](https://csvledger.readthedocs.io/en/latest/Quickstart.html) to get started.


## Installation


### Development setup

To install CSVLedger begin by forking the repo.  Download the fork and switch to the directory.

    cd csvledger

Ensure that poetry is installed on your system.  Then run:

    poetry install --with=dev

Finally install the pre-commit hook.

    pre-commit install


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
