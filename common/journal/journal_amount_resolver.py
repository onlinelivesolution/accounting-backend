from decimal import Decimal

class JournalAmountResolver:

    @staticmethod
    def get_amount(source_object, amount_source: str) -> Decimal:

        value = getattr(source_object, amount_source, 0)

        if value is None:
            return Decimal("0")

        return Decimal(str(value))