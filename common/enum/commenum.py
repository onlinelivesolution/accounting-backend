from enum import Enum

class QuotationFilter(str, Enum):
    ALL = "ALL"
    TODAY = "TODAY"
    THIS_MONTH = "THIS_MONTH"
    EXPIRING_TODAY = "EXPIRING_TODAY"
    EXPIRED = "EXPIRED"
    PENDING = "PENDING"
    INVOICED = "INVOICED"
    
class LoadType(str, Enum):
    BANK = "BANK"
    CASH = "CASH"
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"
    PAYABLE = "PAYABLE"
    RECEIVABLE = "RECEIVABLE"

class DefaultPayrollItem(Enum):
    BasicSalary = 1
    HouseRentAllowance = 2
    MedicalAllowance = 3
    Conveyance = 4
    
class DefaultItemStatus(Enum):
    Applied = 1
    Approved = 2
    Paid = 3
    Cancelled = 4
    Rejected = 5

class GenderName(Enum):
    Male = 1
    Female = 2
    Others = 3

class BankDepositType(Enum):
    Cash = 1
    Cheque = 2

class DefaultPaymentMethod(Enum):
    Cash = 1
    Cheque = 2
    CreditCard = 3
    EFT = 4

class AdvanceOrDueAccounts(Enum):
    AdvanceExpense = 1
    DueExpense = 2
    AdvanceRevenue = 3
    DueRevenue = 4
    
class BankAccountType(Enum):
    Loan = 1
    Current = 2
    Deposit = 3
    
class MonthName(Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12

class DefaultAccount(Enum):
    CashOnHand = 1
    Capital = 2
    Sales = 3
    CostOfGoodSold = 4
    VATExpense = 5
    DiscountEarned = 6
    DiscountGiven = 7
    VATPayable = 8
    AccountsPayable = 9
    AccountReceivable = 10
    Inventory = 11
    Bank = 12
    Salary = 13
    SalaryPayable = 14
    TaxPayable = 15
    EmployeePF = 16
    EmployerPFContribution = 17
    PFBank = 18
    ProfitLoss = 19
    Bonus = 20
    BonusPayable = 21
    ServiceIncome = 22
    ProjectIncome = 23
    EmployeeSupplementaryPF = 24
    EmployeeLoanReceivable = 25
    EmployeeLoanInterest = 26
    AdvanceSalaryReceivable = 27
    FixedAssets = 28
    ExpenseAccount = 29
    DepreciationAccount = 30
    FurnitureAndFixture = 31
    ElectricalEquipment = 32
    OfficeEquipment = 33
    ComputerAndOtherITEquipment = 34
    AirConditioner = 35
    OfficeRenovation = 36
    Vehicles = 37
    LandAndBuildings = 38
    GoodWill = 39
    PreliminaryExpense = 40
    AdvanceDepositsPrepayments = 41
    ProvisionForExpenses = 42
    AuthorizedCapital = 43
    IssuedSubscribedPaidUpCapital = 44
    InterestEarned = 45
    OtherRevenueEarned = 46
    ThirdPartyLoan = 47
    AccruedLoanInterest = 48
    AdvanceExpense = 49
    DueExpense = 50
    Wastage = 51
    VATExpenseForeign = 52
    AccruedServiceIncome = 53
    ThirdPartyPayment = 54
    MaterialExpense = 55
