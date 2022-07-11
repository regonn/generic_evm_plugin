import datetime
import time
from math import floor

import requests

from util.generic_evm_transaction import GenericEvmTransaction


class CovalentClient:
    CHAIN_ID_MAP = {"bsc": "56"}

    @classmethod
    def get_transactions(
        cls, chain, settings, transaction_params
    ) -> list[GenericEvmTransaction]:
        transactions = []

        page = 0
        page_size = 1000
        while True:
            txs = cls.get_txs(
                settings["covalent_api_key"],
                chain,
                transaction_params["data"],
                page,
                page_size,
            )

            for tx in txs:
                if transaction_params["data"].lower() in [
                    tx["from_address"].lower(),
                    tx["to_address"].lower(),
                ]:
                    transactions.append(
                        GenericEvmTransaction(
                            chain,
                            tx["tx_hash"],
                            floor(
                                time.mktime(
                                    datetime.datetime.strptime(
                                        tx["block_signed_at"], "%Y-%m-%dT%H:%M:%SZ"
                                    ).timetuple()
                                )
                            ),
                            tx["fees_paid"]
                            if tx["from_address"].lower()
                            == transaction_params["data"].lower()
                            else "0.0",
                            tx["from_address"],
                            tx["to_address"],
                            "BNB",
                            tx["value"],
                        )
                    )
            page += 1
            if len(txs) < page_size:
                break

        return transactions

    @classmethod
    def get_txs(
        cls,
        api_key: str,
        chain: str,
        address: str,
        page_number: int = 0,
        page_size: int = 1000,
    ) -> list:
        headers = {
            "Content-Type": "application/json",
        }

        params = {
            "page-number": str(page_number),
            "page-size": str(page_size),
            "no-logs": "true",
        }

        chain_number = cls.CHAIN_ID_MAP[chain]

        response = requests.get(
            f"https://api.covalenthq.com/v1/{chain_number}/address/{address}/transactions_v2/",
            params=params,
            headers=headers,
            auth=(api_key, ""),
        )
        return response.json()["data"]["items"]
