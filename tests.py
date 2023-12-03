from tax_calculation import (
    calculate_tax_free_allowance_based_on_children,
    calculate_tax_free_allowance_based_on_elder,
    calculate_tax_free_allowance,
    get_income_tax_percent_rate_and_border_leftover,
    get_income_tax_rates_for_receipt_parts,
    get_income_tax_amount,
    calculate_income_tax,
    perform_calculations,
    get_social_security_deductions_amount,
)
from enums import IncomeTaxBorder, Month


def test_calculate_tax_free_allowance_based_on_children():
    assert calculate_tax_free_allowance_based_on_children(children_count=1) == 2400
    assert (
        calculate_tax_free_allowance_based_on_children(children_count=2) == 2400 + 2700
    )
    assert (
        calculate_tax_free_allowance_based_on_children(children_count=3)
        == 2400 + 2700 + 4000
    )
    assert (
        calculate_tax_free_allowance_based_on_children(children_count=4)
        == 2400 + 2700 + 4000 + 4500
    )
    assert (
        calculate_tax_free_allowance_based_on_children(children_count=5)
        == 2400 + 2700 + 4000 + 4500 + 2800
    )
    assert (
        calculate_tax_free_allowance_based_on_children(children_count=6)
        == 2400 + 2700 + 4000 + 4500 + 2800 * 2
    )


def test_calculate_tax_free_allowance_based_on_elder():
    over_65_count = 3
    over_75_count = 2
    annual_income = 7000
    assert (
        calculate_tax_free_allowance_based_on_elder(
            over_65_count=3,
            over_75_count=2,
            annual_income=annual_income,
        )
        == 1150 * over_65_count + 2550 * over_75_count
    )
    assert (
        calculate_tax_free_allowance_based_on_elder(
            over_65_count=3,
            over_75_count=2,
            annual_income=annual_income + 1000,
        )
        == 0
    )


def test_calculate_tax_free_allowance():
    annual_income = 35000
    children_count = 2
    over_65_count = 1
    over_75_count = 0

    assert (
        calculate_tax_free_allowance(
            annual_income=annual_income,
            children_count=children_count,
            over_65_count=over_65_count,
            over_75_count=over_75_count,
        )
        == 5100
    )


def test_get_income_tax_percent_rate_and_border_leftover():
    income_under_19_percent = 10000
    income_equal_19_percent = 12450
    income_under_24_percent = 20000
    income_under_30_percent = 30000
    income_under_37_percent = 40000
    income_under_45_percent = 100000
    income_under_47_percent = 350000

    assert (
        get_income_tax_percent_rate_and_border_leftover(income_under_19_percent)
        == IncomeTaxBorder.BORDER_19_PERCENT.value[1],
        IncomeTaxBorder.BORDER_19_PERCENT.value[0] - income_under_19_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_equal_19_percent)
        == IncomeTaxBorder.BORDER_24_PERCENT.value[1],
        IncomeTaxBorder.BORDER_24_PERCENT.value[0] - income_equal_19_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_equal_19_percent)
        == IncomeTaxBorder.BORDER_24_PERCENT.value[1],
        IncomeTaxBorder.BORDER_24_PERCENT.value[0] - income_equal_19_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_under_24_percent)
        == IncomeTaxBorder.BORDER_24_PERCENT.value[1],
        IncomeTaxBorder.BORDER_24_PERCENT.value[0] - income_under_24_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_under_30_percent)
        == IncomeTaxBorder.BORDER_30_PERCENT.value[1],
        IncomeTaxBorder.BORDER_30_PERCENT.value[0] - income_under_30_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_under_37_percent)
        == IncomeTaxBorder.BORDER_37_PERCENT.value[1],
        IncomeTaxBorder.BORDER_37_PERCENT.value[0] - income_under_37_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_under_45_percent)
        == IncomeTaxBorder.BORDER_45_PERCENT.value[1],
        IncomeTaxBorder.BORDER_45_PERCENT.value[0] - income_under_45_percent,
    )
    assert (
        get_income_tax_percent_rate_and_border_leftover(income_under_47_percent)
        == IncomeTaxBorder.BORDER_47_PERCENT.value[1],
        IncomeTaxBorder.BORDER_47_PERCENT.value[0] - income_under_47_percent,
    )


def test_get_income_tax_rates_for_receipt_parts():
    total_income_before_receipt = 10000
    receipt = 10000
    lower_tax_rate_income_part = (
        IncomeTaxBorder.BORDER_19_PERCENT.value[0] - total_income_before_receipt
    )
    higher_tax_rate_income_part = receipt - lower_tax_rate_income_part
    assert get_income_tax_rates_for_receipt_parts(
        total_income_before_receipt, receipt
    ) == [
        (IncomeTaxBorder.BORDER_19_PERCENT.value[1], lower_tax_rate_income_part),
        (IncomeTaxBorder.BORDER_24_PERCENT.value[1], higher_tax_rate_income_part),
    ]


def test_get_income_tax_amount():
    assert (
        get_income_tax_amount(
            [
                (IncomeTaxBorder.BORDER_19_PERCENT.value[1], 10000),
                (IncomeTaxBorder.BORDER_24_PERCENT.value[1], 10000),
            ]
        )
        == 1900 + 2400
    )


def test_calculate_income_tax():
    monthly_salary = 3000
    annual_receipts_count = 15
    tax_free_allowances = 2400

    result_dict = calculate_income_tax(
        monthly_salary, annual_receipts_count, tax_free_allowances
    )
    assert result_dict[Month.JAN]["income_tax_amount"] == 114
    assert result_dict[Month.FEB]["income_tax_amount"] == 570
    assert result_dict[Month.MAR]["income_tax_amount"] == 570
    assert result_dict[Month.APR]["income_tax_amount"] == 570
    assert result_dict[Month.MAY]["income_tax_amount"] == 577.5
    assert result_dict[Month.JUN]["income_tax_amount"] == 720
    assert result_dict[Month.JUL]["income_tax_amount"] == 720
    assert result_dict[Month.AUG]["income_tax_amount"] == 804
    assert result_dict[Month.SEP]["income_tax_amount"] == 900
    assert result_dict[Month.OCT]["income_tax_amount"] == 900
    assert result_dict[Month.NOV]["income_tax_amount"] == 900
    assert result_dict[Month.DEC]["income_tax_amount"] == 4118


def test_perform_calculations():
    salary_pln = 3000 * 4.7
    rate = 4.7
    annual_receipts_count = 15
    children_count = 1
    result_dict = perform_calculations(
        salary_other_currency=salary_pln,
        rate=rate,
        annual_receipts=annual_receipts_count,
        children_count=children_count,
    )
    assert result_dict[Month.JAN][
        "receipt_netto"
    ] == 2886 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.FEB][
        "receipt_netto"
    ] == 2430 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.MAR][
        "receipt_netto"
    ] == 2430 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.APR][
        "receipt_netto"
    ] == 2430 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.MAY][
        "receipt_netto"
    ] == 2422.5 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.JUN][
        "receipt_netto"
    ] == 2280 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.JUL][
        "receipt_netto"
    ] == 2280 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.AUG][
        "receipt_netto"
    ] == 2196 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.SEP][
        "receipt_netto"
    ] == 2100 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.OCT][
        "receipt_netto"
    ] == 2100 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.NOV][
        "receipt_netto"
    ] == 2100 - get_social_security_deductions_amount(salary_pln / 4.7)
    assert result_dict[Month.DEC][
        "receipt_netto"
    ] == 7882 - get_social_security_deductions_amount(salary_pln * 3 / 4.7)


def test_perform_calculations_less_than_12_receipts():
    salary_pln = 3000 * 4.7
    rate = 4.7
    annual_receipts_count = 10
    children_count = 1
    result_dict = perform_calculations(
        salary_other_currency=salary_pln,
        rate=rate,
        annual_receipts=annual_receipts_count,
        children_count=children_count,
    )
    assert len(result_dict) == annual_receipts_count
