from util.covalent_client import CovalentClient
from util.explorer_client import ExplorerClient
from util.generic_evm_transaction import GenericEvmTransaction

CHAIN_NATIVE_TOKEN_MAP = {
    "bsc": "bnb",
}


class TransactionGenerator:
    @classmethod
    def get_transactions(
        cls, chain, transaction_params: dict
    ) -> list[GenericEvmTransaction]:
        settings = transaction_params["settings"].get_settings()
        transactions = CovalentClient.get_transactions(
            chain, settings, transaction_params
        )

        if chain == "bsc":
            transactions.extend(
                ExplorerClient.get_transactions(
                    chain, settings["explorer_api_key"], transaction_params["data"]
                )
            )

        return transactions
