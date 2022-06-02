import argparse

import pandas as pd
from senkalib.senka_setting import SenkaSetting
from senkalib.token_original_id_table import TokenOriginalIdTable

from util.transaction_generator import TransactionGenerator
from generic_evm_plugin.generic_evm_plugin import GenericEvmPlugin

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
        default=None,
        help="Covalent API key",
    )
    chain = parser.parse_args().chain
    address = parser.parse_args().address
    caajs = []
    settings = SenkaSetting({"covalent_api_key": parser.parse_args().covalent_api_key})
    token_original_ids = TokenOriginalIdTable(TOKEN_ORIGINAL_IDS_URL)
    transactions = TransactionGenerator.get_transactions(
        chain, {"settings": settings, "data": address}
    )

    for transaction in transactions:
        if GenericEvmPlugin.can_handle(transaction):
            caaj_peace = GenericEvmPlugin.get_caajs(
                chain, address, transaction, token_original_ids
            )
            caajs.extend(caaj_peace)

    df = pd.DataFrame(caajs)
    df = df.sort_values("executed_at")
    caaj_csv = df.to_csv(None, index=False)
    print(caaj_csv)
