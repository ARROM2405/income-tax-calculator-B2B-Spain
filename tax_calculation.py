from enums import IncomeTaxBorder, Month
from utils import if_negative_convert_to_zero

SALARY_IN_OTHER_CURRENCY = None
SALARY_IN_EUR = None

OTHER_CURRENCY_TO_EUR_RATE = None

CHILDREN = None
ELDER_OVER_65 = None
ELDER_OVER_75 = None


def convert_salary_to_eur(
    salary_other_curerncy: int | float,
    rate: int | float,
) -> float:
    return salary_other_curerncy / rate


def calculate_tax_free_allowance_based_on_children(children_count: int) -> int:
    tax_free_allowance = 0
    if children_count >= 1:
        tax_free_allowance += 2400
    if children_count >= 2:
        tax_free_allowance += 2700
    if children_count >= 3:
        tax_free_allowance += 4000
    if children_count >= 4:
        tax_free_allowance += 4500
    if children_count > 4:
        tax_free_allowance += (children_count - 4) * 2800
    return tax_free_allowance


def calculate_tax_free_allowance_based_on_elder(
    over_65_count: int,
    over_75_count: int,
    annual_income,
) -> int:
    tax_free_allowance = 0
    if annual_income < 8000:
        tax_free_allowance += over_65_count * 1150
        tax_free_allowance += over_75_count * 2550
    return tax_free_allowance


def calculate_tax_free_allowance(
    annual_income: int | float,
    children_count: int = 0,
    over_65_count: int = 0,
    over_75_count: int = 0,
) -> int:
    tax_free_allowance_of_children = calculate_tax_free_allowance_based_on_children(
        children_count
    )
    tax_free_allowance_of_elder = calculate_tax_free_allowance_based_on_elder(
        over_65_count,
        over_75_count,
        annual_income,
    )
    return tax_free_allowance_of_children + tax_free_allowance_of_elder


def get_income_tax_percent_rate_and_border_leftover(
    income: int | float,
) -> tuple[int, int | float]:
    higher_border = IncomeTaxBorder.BORDER_47_PERCENT
    for border in reversed(IncomeTaxBorder):
        if income >= border.value[0]:
            tax_rate = higher_border.value[1]
            left_to_higher_rate_border = higher_border.value[0] - income
            break
        higher_border = border
    else:
        tax_rate = IncomeTaxBorder.BORDER_19_PERCENT.value[1]
        left_to_higher_rate_border = IncomeTaxBorder.BORDER_19_PERCENT.value[0] - income
    return tax_rate, left_to_higher_rate_border


def get_income_tax_rates_for_receipt_parts(
    total_income_before_receipt: int | float, receipt: int | float
) -> list[tuple[int, int | float]]:
    result = []
    income = total_income_before_receipt
    while receipt:
        (
            income_rate,
            left_to_the_higher_border,
        ) = get_income_tax_percent_rate_and_border_leftover(income)

        if receipt >= left_to_the_higher_border:
            taxable_part = left_to_the_higher_border
        else:
            taxable_part = receipt
        result.append((income_rate, taxable_part))
        receipt -= taxable_part
        income += taxable_part

    return result


def get_income_tax_amount(
    tax_rates_and_taxable_amounts: list[tuple[int, int | float]]
) -> int | float:
    tax_amount = 0
    for rate, taxable_amount in tax_rates_and_taxable_amounts:
        tax_amount += taxable_amount * rate / 100
    return tax_amount


def calculate_income_tax(
    monthly_salary: int | float,
    annual_receipts_count: int,
    tax_free_allowances: int | float,
) -> dict[
    Month : dict[
        str : int | float,  # receipt_brutto
        str : int | float,  # income_tax_amount
        str : int | float,  # receipt_netto
        str : int | float,  # tax_free_allowances
        str : int | float,  # total_income
        str : int | float,  # total_taxable_income
        str : list[tuple[int, int | float]],  # tax_rates_and_amount_parts
    ],
]:
    income_tax_dict = {}
    total_income = 0
    taxable_total_income = 0
    extra_receipts = annual_receipts_count - 12
    for month in list(Month)[:annual_receipts_count]:
        if month == Month.DEC and extra_receipts:
            current_month_receipt = monthly_salary * (1 + extra_receipts)
        else:
            current_month_receipt = monthly_salary

        taxable_current_month_receipt = current_month_receipt
        if tax_free_allowances:
            taxable_current_month_receipt -= tax_free_allowances
            taxable_current_month_receipt = if_negative_convert_to_zero(
                taxable_current_month_receipt
            )
            tax_free_allowances -= current_month_receipt - taxable_current_month_receipt
            tax_free_allowances = if_negative_convert_to_zero(tax_free_allowances)

        tax_rates_and_amount_parts = get_income_tax_rates_for_receipt_parts(
            taxable_total_income,
            taxable_current_month_receipt,
        )
        tax_amount = get_income_tax_amount(tax_rates_and_amount_parts)

        taxable_total_income += taxable_current_month_receipt
        total_income += current_month_receipt

        income_tax_dict[month] = {
            "receipt_brutto": current_month_receipt,
            "income_tax_amount": tax_amount,
            "receipt_netto": current_month_receipt - tax_amount,
            "tax_free_allowances": current_month_receipt
            - taxable_current_month_receipt,
            "total_income": total_income,
            "total_taxable_income": taxable_total_income,
            "tax_rates_and_amount_parts": tax_rates_and_amount_parts,
        }

    return income_tax_dict


def get_social_security_deductions_amount(receipt: int | float):
    if receipt < 670:
        return 230
    if receipt <= 900:
        return 260
    if receipt < 1166.7:
        return 275
    if receipt <= 1300:
        return 291
    if receipt <= 1700:
        return 294
    if receipt <= 1850:
        return 310
    if receipt <= 2030:
        return 315
    if receipt <= 2330:
        return 320
    if receipt <= 2760:
        return 330
    if receipt <= 3190:
        return 350
    if receipt <= 3620:
        return 370
    if receipt <= 4050:
        return 390
    if receipt <= 6000:
        return 420
    return 500


def perform_calculations(
    salary_other_currency: int | float = None,
    salary_eur: int | float = None,
    rate: int | float = None,
    annual_receipts: int = 12,
    children_count: int = 0,
    over_65_count: int = 0,
    over_75_count: int = 0,
) -> dict[
    Month : dict[
        str : int | float,  # receipt_brutto
        str : int | float,  # income_tax_amount
        str : int | float,  # receipt_netto
        str : int | float,  # tax_free_allowances
        str : int | float,  # total_income
        str : int | float,  # total_taxable_income
        str : list[tuple[int, int | float]],  # tax_rates_and_amount_parts
        str : int | float,  # social_security_deductions
    ],
]:
    assert (salary_eur and not salary_other_currency) or (
        salary_other_currency and not salary_eur
    )

    if salary_other_currency:
        assert rate is not None

    monthly_salary = (
        salary_eur if salary_eur else convert_salary_to_eur(salary_other_currency, rate)
    )

    annual_income = monthly_salary * annual_receipts

    tax_free_allowance = calculate_tax_free_allowance(
        annual_income=annual_income,
        children_count=children_count,
        over_65_count=over_65_count,
        over_75_count=over_75_count,
    )
    receipts_per_month_with_tax_deductions = calculate_income_tax(
        monthly_salary, annual_receipts, tax_free_allowance
    )
    for month in list(Month)[:annual_receipts]:
        social_security_deductions = get_social_security_deductions_amount(
            receipts_per_month_with_tax_deductions[month]["receipt_brutto"]
        )
        receipts_per_month_with_tax_deductions[month][
            "receipt_netto"
        ] -= social_security_deductions
        receipts_per_month_with_tax_deductions[month][
            "social_security_deductions"
        ] = social_security_deductions
    return receipts_per_month_with_tax_deductions
