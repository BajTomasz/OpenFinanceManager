import numpy as np
import pandas as pd


def read_data(file_path):
    account_number = 0
    with open(file_path, encoding='cp1250') as f:
        lines = f.readlines()
        account_number = lines[20].replace("\xa0;\n", "").replace(" ", "")

    df = pd.read_csv(file_path, sep=';', skiprows=37, skipfooter=5, encoding='cp1250', engine="python")
    df = df.rename(
        columns={
            "#Data operacji": "transaction_date",
            "#Data księgowania": "settlement_date",
            "#Numer konta": "recipient_account",
            "#Nadawca/Odbiorca": "recipient",
            "#Tytuł": "description",
            "#Kwota": "amount",
            "#Saldo po operacji": "balance",
        }
    )
    df["recipient_account"] = df["recipient_account"].str.replace("\'", "")
    df["recipient"] = df["recipient"].str.replace("\'", "").str.replace(" ", "")
    
    df["balance"] = df["balance"].str.replace(",", ".")
    df["balance"] = df["balance"].str.replace(" ", "")
    df["balance"] = pd.to_numeric(df["balance"])

    df["amount"] = df["amount"].str.replace(",", ".")
    df["amount"] = df["amount"].str.replace(" ", "")
    df["amount"] = pd.to_numeric(df["amount"])

    df["income"] = np.where(df["amount"] > 0, df["amount"], 0)
    df["expense"] = np.where(df["amount"] < 0, df["amount"], 0)

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
        if len(row["recipient_account"]) == 0 :
            if len(row["recipient"]) != 0:
                data.at[index, "recipient_account"] = row["recipient"]
            else:
                data.at[index, "recipient_account"] = row["description"].split("/")[0]

    return account_number, data.sort_values(by=["transaction_date"])
