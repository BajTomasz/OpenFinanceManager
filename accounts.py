import os
import re

import numpy as np
import pandas as pd

from account import Account


class Accounts:
    accounts_list = []
    recipients = {}
    data_dir = ""

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.find_all_accounts()
        #self.find_all_recipients()
        self.find_all_recipients_and_balance()

    def find_all_accounts(self):
        for file_name in os.listdir(self.data_dir):
            if file_name.endswith(".csv"):
                file_path = os.path.join(self.data_dir, file_name)
                account = Account(file_path)
                self.accounts_list.append(account)

    def find_all_recipients(self):
        new_recipient = ""
        for account in self.accounts_list:
            for row in account.data.index:
                new_recipient = account.data.loc[row]["recipient_account"]
                if new_recipient not in self.recipients.keys():
                    self.recipients[new_recipient] = 0

    def find_all_recipients_and_balance(self):
        self.find_all_recipients()
        for account in self.accounts_list:
            for row in account.data.index:
                self.recipients[account.data.loc[row]["recipient_account"]] += account.data.loc[row]["amount"]

        self.recipients = dict(sorted(self.recipients.items(), key=lambda x: x[1], reverse=True))

    def divide_transactions_into_months(self):
        all_monthly_summaries = pd.DataFrame()
        total_start_balance = 0

        for account in self.accounts_list:
            total_start_balance += account.start_saldo
            account.data['transaction_date'] = pd.to_datetime(account.data['transaction_date'])
            account.data['month'] = account.data['transaction_date'].dt.month

            monthly_summary = account.data.groupby('month').agg(
                total_income=('income', 'sum'),
                total_expenses=('expense', 'sum'),
            ).reset_index()

            all_monthly_summaries = pd.concat([all_monthly_summaries, monthly_summary], ignore_index=True)



        total_summary = all_monthly_summaries.groupby('month').agg(
            total_income=('total_income', 'sum'),
            total_expenses=('total_expenses', 'sum'),
            #start_balance=('start_balance', 'sum')
        ).reset_index()


        full_months = pd.DataFrame({'month': range(1, 13)})
        full_summary = full_months.merge(
            total_summary, on='month', how='left'
        )

        full_summary['total_income'] = full_summary['total_income'].fillna(0)
        full_summary['total_expenses'] = full_summary['total_expenses'].fillna(0)
        full_summary['balance'] = 0
        full_summary.loc[0, 'balance'] = total_start_balance + full_summary.loc[0, 'total_income'] + full_summary.loc[0, 'total_expenses']

        for i in range(1, len(full_summary)):
            full_summary.loc[i, 'balance'] = full_summary.loc[i - 1, 'balance'] + full_summary.loc[i, 'total_income'] + full_summary.loc[i, 'total_expenses']


        print(total_start_balance)

        print(full_summary)
        return full_summary



    # Funkcja do zapisywania kont do pliku xlsx
    def save_to_xlsx(self):
        with pd.ExcelWriter("bank_accounts.xlsx", engine="xlsxwriter") as writer:
            for account in self.accounts_list:
                account.data.to_excel(
                    writer, sheet_name=account.account_number, index=False
                )  # nazwa konta jako nazwa arkusza
            recipients_df = pd.DataFrame(list(self.recipients.items()), columns=["Recipient", "Balance"])
            recipients_df.to_excel(writer, sheet_name="recipients balance", index=False)
            monthly_summary = self.divide_transactions_into_months()
            monthly_summary.to_excel(writer, sheet_name="monthly summary", index=False)


def remove_date(text):
    # Wyrażenie regularne do dopasowania daty w formacie YYYY-MM-DD
    date_pattern = r"\d{4}-\d{2}-\d{2}"

    # Usuwanie daty z napisu
    result = re.sub(date_pattern, "", text)

    # Usunięcie ewentualnych dodatkowych spacji
    result = result.strip()

    return result
