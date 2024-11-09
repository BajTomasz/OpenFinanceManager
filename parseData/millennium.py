import re
import numpy as np
import pandas as pd


def read_data(file_path):
    df = pd.read_csv(file_path)
    account_number = df["Numer rachunku/karty"][0]
    df = df.rename(
        columns={
            "Numer rachunku/karty": "account_number",
            "Data transakcji": "transaction_date",
            "Data rozliczenia": "settlement_date",
            "Na konto/Z konta": "recipient_account",
            "Odbiorca/Zleceniodawca": "recipient",
            "Opis": "description",
            "Obciążenia": "expense",
            "Uznania": "income",
            "Saldo": "balance",
        }
    )
    df["amount"] = df["income"].fillna(0) + df["expense"].fillna(0)
    data = df[
        [
            "transaction_date",
            "settlement_date",
            "recipient",
            "recipient_account",
            "description",
            "income",
            "expense",
            "amount",
            "balance"
        ]
    ]

    for index, row in data.iterrows():
        if pd.isna(row["recipient_account"]):
            if not pd.isna(row["recipient"]):
                data.at[index, "recipient_account"] = row["recipient"]
            else:
                data.at[index, "recipient_account"] = remove_date(row["description"])


    return account_number.replace(" ", ""), data.sort_values(by=["transaction_date"])

def remove_date(text):
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    result = re.sub(date_pattern, "", text)
    result = result.strip()

    return result
