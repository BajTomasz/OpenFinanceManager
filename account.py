import pandas as pd

import parseData.mBank as mbank
import parseData.millennium as millennium
import parseData.pko as pko


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
            "amount",
            "balance",
        ]
    )

    def __init__(self, file_path, bank):
        match bank:
            case "Millennium":
                self.account_number, self.data = millennium.read_data(file_path)
            case "mBank":
                self.account_number, self.data = mbank.read_data(file_path)
            case "PKO":
                self.account_number, self.data = pko.read_data(file_path)

        self.start_saldo = self.data.iloc[0]["balance"] - self.data.iloc[0]["amount"]
        print(self.data)
