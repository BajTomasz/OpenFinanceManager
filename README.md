**How to use:**

The first time you run the application it will generate folders with names that you can use.

Paste your bank statements in CSV files into the appropriate folders and run again.


**Introduction**
------------

This project aims to generate an enriched context for personal finance management by analyzing bank statement files from various banks. It aggregates data from multiple accounts, categorizes transactions, and provides a summary of income and expenses.

The primary goal of this project is to simplify the process of tracking financial information by consolidating data from different bank statements into a single, easily accessible report.

Features
--------

1. **Account Aggregation**: The project can handle multiple accounts from various banks, including Millennium, mBank, and PKO.
2. **Monthly Summary**: A monthly summary of income and expenses is generated for all account.
3. **Balance Tracking**: The project tracks the balance for each account over time, providing a clear view of financial progress.
4. **Recipient Analysis**: It analyzes recipients' names and check balance.

How to Use
----------

1. **Run the Script**: Execute the main.py script to initiate the data aggregation process.
2. **Add data:** Copy your CSV files downloaded from your bank site.
3. **Generate Reports**: The project will generate reports in an Excel file named "bank_accounts.xlsx" with detailed account information, monthly summaries, and balance tracking.

TODO
----

* fix start balance,
* add account_number in PKO (?)
* skipping internal transfers
* add exec files or building scripts
* and many many more
