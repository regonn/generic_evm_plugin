import json

import requests

from util.generic_evm_transaction import GenericEvmTransaction

BSC_SCAN_MAX_PAGE_SIZE = 1000

EXPLOER_CONFIG = {
    "bsc": {
        "base_api_url": "https://api.bscscan.com/api",
        "max_page_size": BSC_SCAN_MAX_PAGE_SIZE,
        "params_set": [
            {
                # Internal Transaction API
                "module": "account",
                "action": "txlistinternal",
                "address": "",
                "page": 0,
                "offset": BSC_SCAN_MAX_PAGE_SIZE,
                "sort": "desc",
                "apikey": "",
            },
            {
                # BEP20 Transaction API
                "module": "account",
                "action": "tokentx",
                "address": "",
                "page": 0,
                "offset": BSC_SCAN_MAX_PAGE_SIZE,
                "sort": "desc",
                "apikey": "",
            },
        ],
    }
}


class ExplorerClient:
    @classmethod
    def get_transactions(
        cls, chain: str, api_key: str, address: str
    ) -> list[GenericEvmTransaction]:
        transactions = []
        for params in EXPLOER_CONFIG[chain]["params_set"]:
            target_params = params.copy()
            target_params["address"] = address.lower()
            target_params["apikey"] = api_key
            page = 1
            while True:
                target_params["page"] = page
                txs = cls.get_txs(EXPLOER_CONFIG[chain]["base_api_url"], target_params)

                page += 1
                for tx in txs:
                    if float(tx["value"]) > 0:
                        transactions.append(
                            GenericEvmTransaction(
                                "bsc",
                                tx["hash"],
                                int(tx["timeStamp"]),
                                "0",
                                tx["from"],
                                tx["to"],
                                "BNB",
                                tx["value"],
                            )
                        )
                if len(txs) < EXPLOER_CONFIG[chain]["max_page_size"]:
                    break
        return transactions

    @classmethod
    def get_txs(cls, url: str, params: dict):
        response = requests.get(url, params=params)
        print(response.text)
        json_response = json.loads(response.text)
        return json_response.get("result")
