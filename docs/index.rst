CSVledger Documentation
=====================================

CSVLedger allows you to take financial transactions downloaded from a bank as a
CSV file and convert the transactions into a ledger journal.  This journal file
can then be processed by `Ledger <https://www.ledger-cli.org>`_.

Turn this:

.. code-block:: SHELL

    Process Dates,Check Number,Description,Credit Amount,Debit Amount
    8/5/2019,,Point of Sale Debit  DATE 08-03 CHICK-FIL-A,,13.28
    8/5/2019,,Point of Sale Debit  DATE 08-03 WAL-MART,,69.98
    8/5/2019,,Point of Sale Debit  DATE 08-03 LIDL,,107.91

Into:

.. code-block:: SHELL

    2019/08/05 * CHICK-FIL-A
		Expenses:Food:Dining	$13.28
		Assets:Checking

    2019/08/05 * WAL-MART
		Expenses:Food:Grocery	$69.98
		Assets:Checking

    2019/08/05 * LIDL
		Expenses:Food:Grocery	$107.91
		Assets:Checking
..


Features
--------

Features include:

* Profiles for different accounts (checking, credit, savings).
* Filtering of excess data from transaction descriptions.
* Automatic categorizing of account categories based on payee descriptions.



.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   Quickstart
   Contributing
   license




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
