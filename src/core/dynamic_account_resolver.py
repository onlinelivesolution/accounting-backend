class DynamicAccountResolver:

    @staticmethod
    def resolve(payment, amount_source: str) -> str | None:

        if not amount_source:
            return None

        mapping = {
            "totalamount": payment.bankAccountCode,
            "taxamount": getattr(payment, "taxAccountCode", None),
            "pfamount": getattr(payment, "pfAccountCode", None),
            "employercontribution": getattr(payment, "employerContributionAccountCode", None),
            "loanadjust": getattr(payment, "loanAccountCode", None),
            "adjustadvancesalary": getattr(payment, "advanceSalaryAccountCode", None),
            "adjustunpaidleave": getattr(payment, "unpaidLeaveAccountCode", None),
        }

        account = mapping.get(amount_source.lower())

        if account:
            return str(account).strip()

        return None