import datetime
import time

from senkalib.platform.bsc.bsc_transaction import BscTransaction
from senkalib.platform.transaction import Transaction
from web3 import Web3

from util.covalent_client import CovalentClient


class TransactionGenerator:
    TRANSACTION_MAP = {
        "bsc": BscTransaction,
    }

    @classmethod
    def get_transactions(cls, chain, transaction_params: dict) -> list[Transaction]:
        settings = transaction_params["settings"].get_settings()
        w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        transactions = []

        transaction_class = cls.TRANSACTION_MAP[chain]

        page = 0
        page_size = 100
        while True:
            txs = CovalentClient.get_transactions(
                settings["covalent_api_key"],
                chain,
                transaction_params["data"],
                page,
                page_size,
            )

            for tx in txs:
                receipt = w3.eth.get_transaction_receipt(tx["tx_hash"])
                transactions.append(
                    transaction_class(
                        tx["tx_hash"],
                        receipt,
                        time.mktime(
                            datetime.datetime.strptime(
                                tx["block_signed_at"], "%Y-%m-%dT%H:%M:%SZ"
                            ).timetuple()
                        ),
                        tx["gas_spent"],
                        tx["gas_price"],
                    )
                )
            page += 1
            if len(txs) < page_size:
                break

        return transactions
