import hashlib
import uuid
from decimal import Decimal

from senkalib.caaj_journal import CaajJournal
from senkalib.token_original_id_table import TokenOriginalIdTable

from util.generic_evm_transaction import GenericEvmTransaction

MEGA = 10**6
EXA = 10**18


class GenericEvmPlugin:
    CHAINS = ["bsc"]

    @classmethod
    def can_handle(cls, chain: str) -> bool:
        return chain in cls.CHAINS

    @classmethod
    def get_caajs(
        cls,
        chain: str,
        address: str,
        transaction: GenericEvmTransaction,
        token_table: TokenOriginalIdTable,
    ) -> list[CaajJournal]:
        caajs = []
        trade_uuid = cls._get_uuid(transaction.transaction_id)
        if transaction.value > 0:
            caajs.append(
                cls._get_caaj(chain, address, transaction, token_table, trade_uuid)
            )

        if transaction.fees_paid > 0:
            caajs.append(
                cls._get_caaj_fee(chain, address, transaction, token_table, trade_uuid)
            )
        return caajs

    @classmethod
    def _get_uuid(cls, transaction_id: str) -> str:
        m = hashlib.md5()
        m.update(transaction_id.encode("utf-8"))
        return str(uuid.UUID(m.hexdigest()))

    @classmethod
    def _get_token_original_id(cls, chain: str, value: str) -> str:
        if chain == "bsc":
            if value == "BNB":
                value = "bnb"
        return value

    @classmethod
    def _get_caaj(
        cls,
        chain: str,
        address: str,
        transaction: GenericEvmTransaction,
        token_table: TokenOriginalIdTable,
        trade_uuid: str,
    ) -> CaajJournal:
        token_original_id = GenericEvmPlugin._get_token_original_id(
            chain, transaction.token_original_id
        )
        symbol_uti = token_table.get_uti(chain, token_original_id)
        return CaajJournal(
            transaction.get_timestamp(),
            chain,
            "",
            chain,
            transaction.get_transaction_id(),
            trade_uuid,
            "get" if transaction.to_address.lower() == address.lower() else "lose",
            str(transaction.value / Decimal(EXA)),
            symbol_uti,
            transaction.from_address,
            transaction.to_address,
            "",
        )

    @classmethod
    def _get_caaj_fee(
        cls,
        chain: str,
        address: str,
        transaction: GenericEvmTransaction,
        token_table: TokenOriginalIdTable,
        trade_uuid: str,
    ) -> CaajJournal:
        token_original_id = GenericEvmPlugin._get_token_original_id(chain, "bnb")
        symbol_uti = token_table.get_uti(chain, token_original_id)
        return CaajJournal(
            transaction.get_timestamp(),
            chain,
            "",
            chain,
            transaction.get_transaction_id(),
            trade_uuid,
            "lose",
            str(transaction.get_transaction_fee() / Decimal(EXA)),
            symbol_uti,
            address,
            "fee",
            "",
        )
