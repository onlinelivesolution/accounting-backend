# utils/journal_amount_resolver.py

from decimal import Decimal


class JournalAmountResolver:

    @staticmethod
    def get_amount(payment, amount_source: str):

        if not amount_source:
            return Decimal("0")

        amount_source = amount_source.lower()

        if amount_source == "totalamount":
            return Decimal(str(payment.totalAmount or 0))

        elif amount_source == "taxamount":
            return sum(
                Decimal(str(d.taxAmount or 0)) for d in payment.salaryPaymentDetails
            )

        elif amount_source == "pfamount":
            return sum(
                Decimal(str(d.pfAmount or 0)) for d in payment.salaryPaymentDetails
            )

        elif amount_source == "loanadjust":
            return sum(
                Decimal(str(d.loanAdjust or 0)) for d in payment.salaryPaymentDetails
            )

        elif amount_source == "adjustadvancesalary":
            return sum(
                Decimal(str(d.adjustAdvanceSalary or 0))
                for d in payment.salaryPaymentDetails
            )

        elif amount_source == "adjustunpaidleave":
            return sum(
                Decimal(str(d.adjustUnpaidLeave or 0))
                for d in payment.salaryPaymentDetails
            )

        elif amount_source == "otherdeductions":
            return sum(
                Decimal(str(d.otherDeductions or 0))
                for d in payment.salaryPaymentDetails
            )

        return Decimal("0")
