import uuid
from decimal import Decimal

from senkalib.caaj_journal import CaajJournal
from senkalib.chain.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable

MEGA = 10**6
EXA = 10**18


class GenericEvmPlugin:
    CHAINS = ["bsc"]

    @classmethod
    def can_handle(cls, transaction: Transaction) -> bool:
        chain_id = transaction.platform
        return chain_id in cls.CHAINS

    @classmethod
    def get_caajs(
        cls,
        chain: str,
        address: str,
        transaction: Transaction,
        token_table: TokenOriginalIdTable,
    ) -> list[CaajJournal]:
        caajs = []
        trade_uuid = GenericEvmPlugin._get_uuid()
        caaj_fee = GenericEvmPlugin._get_caaj_fee(
            chain, address, transaction, token_table, trade_uuid
        )
        caajs.extend(caaj_fee)
        return caajs

    @classmethod
    def _get_uuid(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def _get_token_original_id(cls, chain: str, value: str) -> str:
        if chain == "bsc":
            if value == "BNB":
                value = "bnb"
        return value

    @classmethod
    def _get_caaj_fee(
        cls,
        chain: str,
        address: str,
        transaction: Transaction,
        token_table: TokenOriginalIdTable,
        trade_uuid: str,
    ) -> list:
        caajs = []
        token_original_id = GenericEvmPlugin._get_token_original_id(chain, "bnb")
        symbol_uti = token_table.get_uti(chain, token_original_id)
        caajs.append(
            CaajJournal(
                transaction.get_timestamp(),
                chain,
                "",
                chain,
                transaction.get_transaction_id(),
                trade_uuid,
                "lose",
                str(transaction.get_transaction_fee() / Decimal(MEGA)),
                symbol_uti,
                address,
                "fee",
                "",
            )
        )
        return caajs
