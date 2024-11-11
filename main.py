import os

from accounts import Accounts


def main():
    create_dirs_supported_banks()
    accounts = Accounts()
    accounts.save_to_xlsx()


def create_dirs_supported_banks():
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/Millennium"):
        os.mkdir("data/Millennium")
    if not os.path.exists("data/mBank"):
        os.mkdir("data/mBank")
    if not os.path.exists("data/PKO"):
        os.mkdir("data/PKO")


if __name__ == "__main__":
    main()
