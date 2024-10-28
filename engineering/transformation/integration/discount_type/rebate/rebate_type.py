import pandas as pd

from engineering.transformation.integration.binnacle import BinnacleIntegrator
from engineering.transformation.integration.discount_type.rebate.rebate import RebateSellinIntegrator
from engineering.transformation.integration.discount_type.summary import generate_summary_rebate_sheet
from engineering.transformation.integration.utils.utils import generate_base_months_sheets
from schemas.request.options import Options


def generate_rebate_sheets(
    data: dict[str, pd.DataFrame],
    options: Options,
    list_month: list[str]
) -> dict[str, pd.DataFrame]:
    """
    Generate the sheets for the rebate report

    :param data: The data to generate the sheets
    :type data: dict[str, pd.DataFrame]
    :param options: The options selected by the user
    :type options: dict[str, Any]
    :param list_month: The list of months to generate the sheets
    :type list_month: list[str]
    :return: The sheets for the rebate report
    :rtype: dict[str, pd.DataFrame]
    """
    binnacle: pd.DataFrame = data["binnacle"].copy()
    sellin: pd.DataFrame = data["sales"].copy()
    if options.nodo == "D. COPACIGULF":
        binnacle = BinnacleIntegrator.create_lower_tm_column(binnacle)
        binnacle = BinnacleIntegrator.create_upper_tm_column(binnacle)
        binnacle = BinnacleIntegrator.create_mean_tm_column(binnacle, sellin)
    else:
        binnacle = BinnacleIntegrator.create_validators_column(binnacle, sellin)
        application = BinnacleIntegrator.get_type_application(binnacle)
        rebate: RebateSellinIntegrator = RebateSellinIntegrator()
        sellin = rebate.merge_dataframes(sellin, binnacle)
        if application == "TMS":
            sellin['Bonificación'] = pd.to_numeric(sellin['Bonificación'].apply(
                lambda x: str(x).replace("$", "").replace(",", "")
            ))
        else:
            sellin = rebate.add_pvp_column(sellin)
            sellin = rebate.add_discount_column(sellin)
            sellin = rebate.add_credit_column(sellin)
            sellin = rebate.add_additional_discount_column(sellin)

        sellin = rebate.add_contribution_column(sellin, application)

    base_sheets: dict[str, pd.DataFrame] = generate_base_months_sheets(sellin, options, list_month)
    summary_sheet: dict[str, pd.DataFrame] = generate_summary_rebate_sheet(sellin, binnacle, options)
    dict_sheets: dict[str, pd.DataFrame] = {**base_sheets, **summary_sheet}
    return dict_sheets
