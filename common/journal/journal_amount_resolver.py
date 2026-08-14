from decimal import Decimal


class JournalAmountResolver:

    @staticmethod
    def _sum_details(details, field_name: str) -> Decimal:

        if not details:
            return Decimal("0")

        total = Decimal("0")

        for detail in details:

            value = getattr(detail, field_name, 0)

            if value is None:
                value = 0

            total += Decimal(str(value))

        return total

    @staticmethod
    def get_amount(source_object, amount_source: str) -> Decimal:

        if not amount_source:
            return Decimal("0")

        amount_source = amount_source.strip().lower()

        # ==================================================
        # Salary Generation
        # ==================================================
        details = getattr(source_object, "details", None)

        # ==================================================
        # Salary Payment
        # ==================================================
        if details is None:
            details = getattr(source_object, "salaryPaymentDetails", None)

        details = details or []

        print("--------------------------------")
        print("Journal Amount Resolver")
        print("Amount Source :", amount_source)
        print("Detail Count  :", len(details))
        print("--------------------------------")

        # ==================================================
        # Basic Salary
        # ==================================================
        if amount_source == "basicsalary":
            return JournalAmountResolver._sum_details(details, "basicSalary")

        # ==================================================
        # House Rent
        # ==================================================
        if amount_source in (
            "houserent",
            "houserentallowance",
        ):
            return JournalAmountResolver._sum_details(details, "houseRentAllowance")

        # ==================================================
        # Medical
        # ==================================================
        if amount_source in (
            "medical",
            "medicalallowance",
        ):
            return JournalAmountResolver._sum_details(details, "medicalAllowance")

        # ==================================================
        # Conveyance
        # ==================================================
        if amount_source in (
            "conveyance",
            "conveyanceallowance",
        ):
            return JournalAmountResolver._sum_details(details, "conveyance")

        # ==================================================
        # Overtime
        # ==================================================
        if amount_source == "overtime":
            return JournalAmountResolver._sum_details(details, "overtime")

        # ==================================================
        # Other Allowance
        # ==================================================
        if amount_source == "otherallowance":
            return JournalAmountResolver._sum_details(details, "otherAllowance")

        # ==================================================
        # Gross Earnings
        # ==================================================
        if amount_source in (
            "gross",
            "grossearnings",
        ):
            return JournalAmountResolver._sum_details(details, "grossEarnings")

        # ==================================================
        # Tax
        # ==================================================
        if amount_source == "taxamount":
            return JournalAmountResolver._sum_details(details, "taxAmount")

        # ==================================================
        # PF
        # ==================================================
        if amount_source == "pfamount":
            return JournalAmountResolver._sum_details(details, "pfAmount")

        # ==================================================
        # Employer Contribution
        # ==================================================
        if amount_source == "employercontribution":
            return JournalAmountResolver._sum_details(details, "employerContribution")

        # ==================================================
        # Loan
        # ==================================================
        if amount_source == "loanadjust":
            return JournalAmountResolver._sum_details(details, "loanAdjust")

        # ==================================================
        # Advance Salary
        # ==================================================
        if amount_source == "adjustadvancesalary":
            return JournalAmountResolver._sum_details(details, "adjustAdvanceSalary")

        # ==================================================
        # Unpaid Leave
        # ==================================================
        if amount_source == "adjustunpaidleave":
            return JournalAmountResolver._sum_details(details, "adjustUnpaidLeave")

        # ==================================================
        # House Rent Deduction
        # ==================================================
        if amount_source == "houserentdeduction":
            return JournalAmountResolver._sum_details(details, "houseRentDeduction")

        # ==================================================
        # Excess Mobile Bill
        # ==================================================
        if amount_source == "excessmobilebill":
            return JournalAmountResolver._sum_details(details, "excessMobileBill")

        # ==================================================
        # Other Deduction
        # ==================================================
        if amount_source in (
            "otherdeduction",
            "otherdeductions",
        ):
            return JournalAmountResolver._sum_details(details, "otherDeduction")

        # ==================================================
        # Net Earnings
        # ==================================================
        if amount_source in (
            "netearning",
            "netearnings",
        ):
            return JournalAmountResolver._sum_details(details, "netEarnings")

        # ==================================================
        # Salary Payment Total
        # ==================================================
        if amount_source == "totalamount":

            total_amount = getattr(source_object, "totalAmount", 0)

            return Decimal(str(total_amount or 0))

        print(f"WARNING: Unknown journal amount source: " f"{amount_source}")

        return Decimal("0")
