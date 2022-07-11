import datetime
from decimal import Decimal

from senkalib.platform.transaction import Transaction


class GenericEvmTransaction(Transaction):
    def __init__(
        self,
        platform: str,
        transaction_id: str,
        timestamp: int,
        fees_paid: str,
        from_address: str,
        to_address: str,
        token_original_id: str,
        value: str,
    ):
        super().__init__(transaction_id)
        self.platform = platform
        self.timestamp = timestamp
        self.fees_paid = Decimal(fees_paid)
        self.from_address = from_address
        self.to_address = to_address
        self.token_original_id = token_original_id
        self.value = Decimal(value)

    def get_timestamp(self) -> str:
        return str(
            datetime.datetime.fromtimestamp(
                self.timestamp, datetime.timezone.utc
            ).replace(tzinfo=None)
        )

    def get_transaction_fee(self) -> Decimal:
        return self.fees_paid
