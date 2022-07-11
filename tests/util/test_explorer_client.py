import unittest
from unittest.mock import patch

from util.explorer_client import ExplorerClient
from util.generic_evm_transaction import GenericEvmTransaction


class TestExplorerClient(unittest.TestCase):
    def test_get_transaction(self):
        with patch.object(
            ExplorerClient,
            "get_txs",
            new=TestExplorerClient.mock_get_txs,
        ):
            params = {}
            txs = ExplorerClient.get_txs("url", params)

            assert len(txs) == 0

    @classmethod
    def mock_get_txs(
        cls,
        url: str,
        params: dict,
    ) -> list[GenericEvmTransaction]:

        return []


if __name__ == "__main__":
    unittest.main()
