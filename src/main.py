import argparse

import pandas as pd
from senkalib.senka_setting import SenkaSetting
from senkalib.token_original_id_table import TokenOriginalIdTable

from generic_evm_plugin.generic_evm_plugin import GenericEvmPlugin
from util.transaction_generator import TransactionGenerator

TOKEN_ORIGINAL_IDS_URL = "https://raw.githubusercontent.com/ca3-caaip/token_original_id/master/token_original_id.csv"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genetic EVM plugin")
    parser.add_argument(
        "chain",
        type=str,
        help="EVM chain name",
        choices=GenericEvmPlugin.CHAINS,
    )
    parser.add_argument(
        "address",
        type=str,
        help="EVM address",
    )
    parser.add_argument(
        "covalent_api_key",
        type=str,
        help="Covalent API key",
    )
    parser.add_argument(
        "--explorer_api_key", type=str, help="Blockchain Explorer API key"
    )

    chain = parser.parse_args().chain
    if not GenericEvmPlugin.can_handle(chain):
        raise ValueError(f"{chain} is not supported")
    address = parser.parse_args().address
    explorer_api_key = parser.parse_args().explorer_api_key
    caajs = []
    setting_dict = {"covalent_api_key": parser.parse_args().covalent_api_key}
    if chain == "bsc":
        if explorer_api_key is None:
            raise Exception("--explorer_api_key (BscSan API key) is required")
        setting_dict["explorer_api_key"] = explorer_api_key

    settings = SenkaSetting(setting_dict)
    token_original_ids = TokenOriginalIdTable(TOKEN_ORIGINAL_IDS_URL)
    transactions = TransactionGenerator.get_transactions(
        chain, {"settings": settings, "data": address}
    )
    caajs = []
    for transaction in transactions:
        caajs.extend(
            GenericEvmPlugin.get_caajs(chain, address, transaction, token_original_ids)
        )

    df = pd.DataFrame(caajs)
    df["amount"] = df["amount"].astype(float)
    df = df.sort_values("executed_at")
    caaj_csv = df.to_csv(None, index=False)
    print(caaj_csv)
