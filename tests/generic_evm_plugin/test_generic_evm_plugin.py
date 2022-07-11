import unittest

from senkalib.token_original_id_table import TokenOriginalIdTable

from generic_evm_plugin.generic_evm_plugin import GenericEvmPlugin
from util.generic_evm_transaction import GenericEvmTransaction

TOKEN_ORIGINAL_IDS_URL = "https://raw.githubusercontent.com/ca3-caaip/token_original_id/master/token_original_id.csv"


class TestGenericEvmPlugin(unittest.TestCase):
    def test_can_handle(self):
        self.assertTrue(GenericEvmPlugin.can_handle("bsc"))
        self.assertFalse(GenericEvmPlugin.can_handle("eth"))

    def test_get_uuid(self):
        # Same TransactionHash results in same TradeUUID
        chain = "bsc"
        address = "0xDa28ecfc40181a6DAD8b52723035DFba3386d26E"
        transaction_id1 = (
            "0x4226b740386197d43d37a2178f51a4b8f75a5649c7fc739e7f1f7ec5af57584a"
        )
        transaction_id2 = (
            "0x3b6051506be7c46904aff4ad69ad6f6bfe4397e07f5b75cb0b38831dac687544"
        )
        transaction1 = GenericEvmTransaction(
            chain,
            transaction_id1,
            0,
            "0.1",
            "0xDa28ecfc40181a6DAD8b52723035DFba3386d26E",
            "0xa3bde96ef0038e1fb2fb8d4d8366e1c426a3e6b3",
            "BNB",
            "0.01",
        )
        transaction2 = GenericEvmTransaction(
            chain,
            transaction_id1,
            0,
            "0.1",
            "0xDa28ecfc40181a6DAD8b52723035DFba3386d26E",
            "0xa3bde96ef0038e1fb2fb8d4d8366e1c426a3e6b3",
            "BNB",
            "0.01",
        )
        transaction3 = GenericEvmTransaction(
            chain,
            transaction_id2,
            0,
            "0.1",
            "0xDa28ecfc40181a6DAD8b52723035DFba3386d26E",
            "0xa3bde96ef0038e1fb2fb8d4d8366e1c426a3e6b3",
            "BNB",
            "0.01",
        )
        token_original_ids = TokenOriginalIdTable(TOKEN_ORIGINAL_IDS_URL)

        caaj1 = GenericEvmPlugin.get_caajs(
            chain, address, transaction1, token_original_ids
        )[0]

        caaj2 = GenericEvmPlugin.get_caajs(
            chain, address, transaction2, token_original_ids
        )[0]

        caaj3 = GenericEvmPlugin.get_caajs(
            chain, address, transaction3, token_original_ids
        )[0]

        self.assertEqual(caaj1.trade_uuid, caaj2.trade_uuid)
        self.assertNotEqual(caaj1.trade_uuid, caaj3.trade_uuid)


if __name__ == "__main__":
    unittest.main()
