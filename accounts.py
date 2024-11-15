import os

import numpy as np
import pandas as pd

from account import Account


class Accounts:
    accounts_list = []
    supported_banks = ["Millennium", "mBank", "PKO"]
    recipients = {}
    data_dir = "data"

    def __init__(self):
        self.find_all_accounts()
        # self.find_all_recipients()
        self.find_all_recipients_and_balance()

    def find_all_accounts(self):
        for bank in self.supported_banks:
            data_bank = os.path.join(self.data_dir, bank)
            for file_name in os.listdir(data_bank):
                if file_name.endswith(".csv"):
                    data_bank_file = os.path.join(data_bank, file_name)
                    account = Account(data_bank_file, bank)
                    self.accounts_list.append(account)

    def find_all_recipients(self):
        new_recipient = ""
        for account in self.accounts_list:
            for row in account.data.index:
                new_recipient = account.data.loc[row]["recipient"]
                if new_recipient not in self.recipients.keys():
                    self.recipients[new_recipient] = 0

    def find_all_recipients_and_balance(self):
        self.find_all_recipients()
        for account in self.accounts_list:
            for row in account.data.index:
                self.recipients[account.data.loc[row]["recipient"]] += account.data.loc[row]["amount"]

        self.recipients = dict(sorted(self.recipients.items(), key=lambda x: x[1], reverse=True))

    def divide_transactions_into_months(self):
        all_monthly_summaries = pd.DataFrame()
        total_start_balance = 0

        for account in self.accounts_list:
            total_start_balance += account.start_saldo
            account.data["transaction_date"] = pd.to_datetime(account.data["transaction_date"])
            account.data["month"] = account.data["transaction_date"].dt.month
            account.data["income"] = np.where(account.data["amount"] > 0, account.data["amount"], 0)
            account.data["expense"] = np.where(account.data["amount"] < 0, account.data["amount"], 0)

            monthly_summary = (
                account.data.groupby("month")
                .agg(total_amount=("amount", "sum"), total_income=("income", "sum"), total_expense=("expense", "sum"))
                .reset_index()
            )

            all_monthly_summaries = pd.concat([all_monthly_summaries, monthly_summary], ignore_index=True)

        total_summary = (
            all_monthly_summaries.groupby("month")
            .agg(
                total_amount=("total_amount", "sum"),
                total_income=("total_income", "sum"),
                total_expense=("total_expense", "sum"),
            )
            .reset_index()
        )

        full_months = pd.DataFrame({"month": range(1, 13)})
        full_summary = full_months.merge(total_summary, on="month", how="left")

        full_summary["balance"] = 0
        full_summary.loc[0, "balance"] = total_start_balance + full_summary.loc[0, "total_amount"]

        for i in range(1, len(full_summary)):
            full_summary.loc[i, "balance"] = full_summary.loc[i - 1, "balance"] + full_summary.loc[i, "total_amount"]

        print(total_start_balance)

        print(full_summary)
        return full_summary

    def save_to_xlsx(self):
        with pd.ExcelWriter("bank_accounts.xlsx", engine="xlsxwriter") as writer:
            for account in self.accounts_list:
                account.data.to_excel(writer, sheet_name=account.account_number, index=False)
            recipients_df = pd.DataFrame(list(self.recipients.items()), columns=["Recipient", "Balance"])
            recipients_df.to_excel(writer, sheet_name="recipients balance", index=False)
            monthly_summary = self.divide_transactions_into_months()
            sheet_name = "monthly summary"
            monthly_summary.to_excel(writer, sheet_name=sheet_name, index=False)

            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            chart = workbook.add_chart({"type": "line"})

            for i in range(4):
                col = i + 1
                chart.add_series(
                    {
                        "name": [sheet_name, 0, col],
                        "categories": [sheet_name, 1, 0, 11, 0],
                        "values": [sheet_name, 1, col, 11, col],
                    }
                )

            chart.set_x_axis({"name": "Index"})
            chart.set_y_axis({"name": "Value", "major_gridlines": {"visible": False}})
            worksheet.insert_chart("G2", chart)

        writer.close()
