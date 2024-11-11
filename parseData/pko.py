import re
import numpy as np
import pandas as pd


def read_data(file_path):
    df = pd.read_csv(file_path, sep=',', quotechar='"', encoding='cp1250')
    df_part1 = df.loc[:, ["Data operacji", "Data waluty", "Typ transakcji", "Kwota", "Waluta", "Saldo po transakcji"]]
    df_part2 = df.iloc[:, 6:10]

    def parse_description(df):
        fields = {
            "Lokalizacja :": np.nan,
            "Tytuł :": np.nan,
            "Operacja :": np.nan,
            "Numer telefonu :": np.nan,
            "Nazwa odbiorcy :": np.nan,
            "Rachunek odbiorcy :": np.nan
        }
        
        ordered_df = pd.DataFrame(columns=fields.keys())
        
        rows = []
        for index, row in df.iterrows():
            extracted_values = fields.copy()
            for col_value in row.dropna():
                for key in fields.keys():
                    match = re.search(rf"{re.escape(key)}\s*([^|]+)", col_value)
                    if match:
                        extracted_values[key] = match.group(1).strip()
            rows.append(extracted_values)
        ordered_df = pd.DataFrame(rows, columns=fields.keys())
        return ordered_df
    
    opis_df = parse_description(df_part2)
    data = pd.concat([df_part1, opis_df], axis=1)
    
    data = data.rename(
        columns={
            "Data operacji": "transaction_date",
            "Data waluty": "settlement_date",
            "Nazwa odbiorcy :": "recipient",
            "Rachunek odbiorcy :": "recipient_account",
            "Tytuł :": "description",
            "Kwota": "amount",
            "Saldo po transakcji": "balance",
        }
    )

    for index, row in data.iterrows():
        if row["Typ transakcji"] == "Płatność kartą":
            data["description"][index] = row["Lokalizacja :"]

    for index, row in data.iterrows():
        if pd.isna(row["recipient"]):
            if not pd.isna(row["recipient_account"]):
                data.at[index, "recipient"] = row["recipient_account"]
            elif not pd.isna(row["Numer telefonu :"]):
                data.at[index, "recipient"] = row["Numer telefonu :"]
            else:
                data.at[index, "recipient"] = row["description"]

    data = data[
        [
            "transaction_date",
            "settlement_date",
            "recipient",
            "recipient_account",
            "description",
            "amount",
            "balance"
        ]
    ]                

    return "account_number", data[::-1]
