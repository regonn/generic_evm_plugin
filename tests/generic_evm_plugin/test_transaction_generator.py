import json
import os
import unittest
from pathlib import Path
from typing import Union
from unittest.mock import patch

from senkalib.senka_setting import SenkaSetting
from web3.eth import Eth

from util.covalent_client import CovalentClient
from util.transaction_generator import TransactionGenerator


class TestTransactionGenerator(unittest.TestCase):
    def test_get_transaction(self):
        settings = SenkaSetting({"covalent_api_key": "test"})
        with patch.object(
            CovalentClient,
            "get_transactions",
            new=TestTransactionGenerator.mock_get_transactions,
        ):
            with patch.object(
                Eth,
                "get_transaction_receipt",
                new=TestTransactionGenerator.mock_get_transaction_receipt,
            ):
                transaction_params = {
                    "type": "address",
                    "data": "0x0000000000000000000000000000000000000000",
                    "startblock": 0,
                    "endblock": 0,
                    "settings": settings,
                }
                transactions = TransactionGenerator.get_transactions(
                    "bsc", transaction_params
                )
                timestamp = transactions[0].get_timestamp()
                fee = transactions[0].get_transaction_fee()

                self.assertEqual(timestamp, "2022-01-25 06:34:12")
                self.assertEqual(fee, 373430000000000)

    @classmethod
    def mock_get_transactions(
        cls,
        settings: dict,
        address: str,
        arg_startblock: Union[int, None] = None,
        arg_endblock: Union[int, None] = None,
        arg_page: Union[int, None] = None,
    ):
        mock_transaction = json.loads(
            Path(
                "%s/../testdata/bsc/sample.json" % os.path.dirname(__file__)
            ).read_text()
        )
        return [mock_transaction]

    @classmethod
    def mock_get_transaction_receipt(cls, transaction_hash):
        receipt = json.loads(
            Path(
                "%s/../testdata/bsc/approve.json" % os.path.dirname(__file__)
            ).read_text()
        )
        return receipt


if __name__ == "__main__":
    unittest.main()
