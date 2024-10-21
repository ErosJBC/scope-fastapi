import pandas as pd

from typing import Any
from pydantic import NonPositiveInt
from dash import callback, Input, Output, State

from config.settings import settings
from engineering.engineering import run_generate_data

@callback(  # type: ignore
    [
        Output('download-link', 'href'),  # Update the download link
        Output('download-link', 'download')  # Update the name of the file to download
    ],
    Input('generate-report-button', 'n_clicks'),  # Update the number of clicks of the button 'Generate Report'
    [
        State('nodo-dropdown', 'value'),  # Get the selected value of the node dropdown
        State('discount-type-dropdown', 'value'),  # Get the selected value of the discount type dropdown
        State('year-dropdown', 'value'),  # Get the selected value of the year dropdown
        State('month-dropdown', 'value'),  # Get the selected value of the month dropdown
        Input('sell-in-button', 'n_clicks'),  # Update the number of clicks of the button 'Sell In'
        Input('sell-out-button', 'n_clicks')  # Update the number of clicks of the button 'Sell Out'
    ]
)
def generate_report(
    n_clicks: NonPositiveInt,
    selected_nodo: str,
    selected_type: str,
    selected_year: str,
    selected_month: str,
    sell_in_clicks: NonPositiveInt,
    sell_out_clicks: NonPositiveInt
) -> tuple[str, str]:
    """
    Generate the report based on the selected options

    :param n_clicks: The number of clicks on the 'Generate Report' button
    :type n_clicks: int
    :param selected_nodo: The selected node
    :type selected_nodo: str
    :param selected_type: The selected discount type
    :type selected_type: str
    :param selected_year: The selected year
    :type selected_year: str
    :param selected_month: The selected month
    :type selected_month: str
    :param sell_in_clicks: The number of clicks on the 'Sell In' button
    :type sell_in_clicks: int
    :param sell_out_clicks: The number of clicks on the 'Sell Out' button
    :type sell_out_clicks: int
    :return: The href and the filename of the report
    :rtype: tuple[str, str]
    """
    # Create a dictionary with the options selected by the user
    options: dict[str, Any] = {
        'n_clicks': n_clicks,
        'nodo': selected_nodo,
        'discount_type': selected_type,
        'year': selected_year,
        'month': selected_month,
        'sell_in_clicks': sell_in_clicks,
        'sell_out_clicks': sell_out_clicks
    }
    href, filename = run_generate_data(options, settings)
    return href, filename
