Quickstart
==========


Create the Config
-----------------

After installing, the next step is to configure a config file.  By default, the
config file can be located at `XDG_CONFIG_HOME/csvledger/config.yml`.  For
example, if your XDG_CONFIG_HOME is set to ~/.config then the config file can
be found at `~/.config/csvledger/config.yml`.  Create the file if it doesn't
already exist.

The config file is broken into three main sections.

.. code-block:: YAML

    profile:
    accounts:
    filter:


Profile
~~~~~~~

The profile section will contain all the settings for the csv file.  This is
there transactions are matched to rows of the csv file.  You can create
multiple profiles as needed to match your csv files.  For this example we'll be
using the following csv file:

.. code-block::

    Process Dates,Check Number,Description,Credit Amount,Debit Amount
    8/5/2019,,Point of Sale Debit DATE 08-03 CHICK-FIL-A,,13.28
    8/5/2019,,Point of Sale Debit DATE 08-03 WAL-MART,,69.98
    8/5/2019,,Point of Sale Debit DATE 08-03 LIDL,,107.91


Since our file has a header row, we'll begin by setting header to true.  This
will tell csvledger to skip the first row of the file.

.. code-block:: YAML

    profile:
       default:
           # Set to true if file contains a header row.
           header: true
        accounts:
    filter:

.. note::

    Spacing is very important in YAMl files.  Pay extra attention to idention.

Next we need to match the columns with the columns csvledger expects, which are
date, description, credit, debit.  Begin counting columns with 0.  In our
sample file, the result config would be:


.. code-block:: YAML

    profile:
       default:
           # Set to true if file contains a header row.
           header: true
           # Column number counting starts with 0
           date: 0
           description: 2
           credit: 3
           debit: 4
    accounts:
    filter:


The final section of the profile is the account name.  This is the account that
is funds are deducted from for expense transactions.  In our example, we will
be using `Assets:Checking`.  Therefore our complete profile section of the
config will be:

.. code-block:: YAML

    profile:
       default:
           # Set to true if file contains a header row.
           header: true
           # Column number counting starts with 0
           date: 0
           description: 2
           credit: 3
           debit: 4
           account: "Assets:Checking"
    accounts:
    filter:

Accounts
~~~~~~~~

The second section of the config file is the accounts section.   The accounts
section is where you map ledger accounts to payee information.  For example, to
map the CHICK-FIL-A to Expenses:Dining you'd do the following.


.. code-block:: YAML

    profile:
       default:
    accounts:
    - Expenses:Food:Dining:
      - CHICK-FIL-A
    filter:

.. note::
    The first account category under accounts *must* start with a `-`.
    Addational categories do not start with a `-`.

Adding the additional payee the formatting would result in:

.. code-block:: YAML

    profile:
       default:
    accounts:
    - Expenses:Food:Dining:
      - CHICK-FIL-A
      Expenses:Food:Grocery:
      - LIDL
      - WAL-MART
    filter:




Filtering
~~~~~~~~~

The third and final category in the config is filtering.  This is where you
setup anything you want removed from the transaction description.  There are
two types of filtering options, simple and regex.  Simple filtering just
removes any matching text.  Regex allows for more complicated filtering.

.. code-block::

    Process Dates,Check Number,Description,Credit Amount,Debit Amount
    8/5/2019,,Point of Sale Debit DATE 08-03 CHICK-FIL-A,,13.28
    8/5/2019,,Point of Sale Debit DATE 08-03 WAL-MART,,69.98
    8/5/2019,,Point of Sale Debit DATE 08-03 LIDL,,107.91

Looking at our cvs file, it looks like we can user simple filtering to filter out "Point of Sale",
"Debit" and "DATE.


.. code-block:: YAML

    filter:
      simple:
        - Point of Sale
        - DATE
        - Debit

To remove the "08-03" we will need to use regular expressions.  In this case
the regular expression will be  "\d\d[-]\d\d".  We will add this to the config
under the "regex" heading.


.. code-block:: YAML

    filter:
        simple:
          - point of sale
          - date
          - debit
        regex:
          - \d\d[-]\d\d

Putting it all together
~~~~~~~~~~~~~~~~~~~~~~~

The config file is now completed.  It should look like the following:


.. code-block:: YAML

    profile:
       default:
           # Set to true if file contains a header row.
           header: true
           # Column number counting starts with 0
           date: 0
           description: 2
           credit: 3
           debit: 4
    accounts:
    - Expenses:Food:Dining:
      - CHICK-FIL-A
      Expenses:Food:Grocery:
      - LIDL
      - WAL-MART
    filter:
      simple:
        - point of sale
        - date
        - debit
      regex:
         - \d\d[-]\d\d


Running the config against the transactions file the ledger output is generated.

.. code-block:: SHELL

    csvledger -i transactions.csv

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


If the output is filtered and formatted correctly you can then pipe the output
to a file.

.. code-block:: SHELL

    csvledger -i transactions.csv  > checking.ldg

For further information see `csvledger --help`.
