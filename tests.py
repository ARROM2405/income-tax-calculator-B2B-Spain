from tax_calculation import (
    calculate_tax_free_allowance_based_on_children,
    calculate_tax_free_allowance_based_on_elder,
)


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
