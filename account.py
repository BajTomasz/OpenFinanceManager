import pandas as pd

import parseData.millennium as millennium


class Account:
    start_saldo = 0
    account_number = 0
    data = pd.DataFrame(
        columns=[
            "account_number",
            "transaction_date",
            "settlement_date",
            "recipient",
            "recipient_account",
            "description",
            "income",
            "expense",
            "amount",
            "balance",
        ]
    )

    def __init__(self, file_path):
        # recognize bank
        self.account_number, self.data = millennium.read_millenium_data(file_path)
        self.find_start_saldo()
        print(self.data)
        # injection start saldo

    def find_start_saldo(self):
        self.start_saldo = self.data.iloc[0]["balance"] - self.data.iloc[0]["amount"]
