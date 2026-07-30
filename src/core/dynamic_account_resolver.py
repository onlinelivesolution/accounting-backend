# utils/dynamic_account_resolver.py


class DynamicAccountResolver:

    @staticmethod
    def resolve(payment, amount_source: str):

        if not amount_source:
            return None

        amount_source = amount_source.lower()

        mapping = {
            # Bank / Cash
            "totalamount": payment.bankAccountCode,
            # Future dynamic accounts
            "taxamount": getattr(payment, "taxAccountCode", None),
            "pfamount": getattr(payment, "pfAccountCode", None),
            "loanadjust": getattr(payment, "loanAccountCode", None),
            "adjustadvancesalary": getattr(
                payment,
                "advanceSalaryAccountCode",
                None,
            ),
            "adjustunpaidleave": getattr(
                payment,
                "unpaidLeaveAccountCode",
                None,
            ),
        }

        return mapping.get(amount_source)
