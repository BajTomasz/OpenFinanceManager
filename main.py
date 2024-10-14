from accounts import Accounts


def main():
    accounts = Accounts("data")
    accounts.save_to_xlsx()
    # account.save_to_xlex()
    # di = account.find_all_recipients_and_balance()
    # di = sorted(di.items(), key=lambda x: x[1], reverse=True)
    # for x in di:
    #    print(x)
    # print("Obciążenia: ", income.sum())
    # print("Uznania: ", expenses.sum())
    # print("Saldo: ", calculate_final_saldo(data))


if __name__ == "__main__":
    main()
