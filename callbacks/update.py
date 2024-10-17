from typing import Any
from dash import callback, Input, Output

@callback(
    [
        Output("nodo-dropdown", "options"),
        Output("discount-type-dropdown", "options"),
        Output("year-dropdown", "options"),
        Output("month-dropdown", "options"),
        Output("sell-in-button", "className"),
        Output("sell-out-button", "className"),
    ],
    [
        Input("sell-in-button", "n_clicks"),
        Input("sell-out-button", "n_clicks"),
        Input("nodo-dropdown", "value"),
        Input("year-dropdown", "value"),
    ],
)
def update_dropdowns(sell_in_clicks, sell_out_clicks, selected_nodo, selected_year):
    # Determinar cuál botón fue presionado
    if sell_in_clicks < sell_out_clicks:
        selected_liquidacion = 'Sell Out'
        sell_in_class = "btn btn-secondary"
        sell_out_class = "btn btn-primary"
    else:
        selected_liquidacion = 'Sell In'
        sell_in_class = "btn btn-primary"
        sell_out_class = "btn btn-secondary"

    # Filtrar la bitácora según la liquidación seleccionada y nodos que existan en el maestro de ventas
    filtered_df = bit[(bit['SI/SO'] == selected_liquidacion) & (bit['COD_ZNJE'].isin(rvn['COD_ZNJE'].unique()))]

    # Filtrar el maestro de ventas con nodos que existan en la bitácora
    rvn_filtered = rvn[rvn['COD_ZNJE'].isin(filtered_df['COD_ZNJE'].unique())] if selected_liquidacion == 'Sell In' else \
    rvn_so[rvn_so['COD_ZNJE'].isin(filtered_df['COD_ZNJE'].unique())]

    # Generar opciones actualizadas para el dropdown de 'Nodo'
    nodo_options = [{'label': nodo, 'value': nodo} for nodo in filtered_df['DES_ZNJE'].unique()]

    # Filtrar bitácora y maestro de ventas según el nodo seleccionado
    if selected_nodo:
        filtered_df = filtered_df[filtered_df['DES_ZNJE'] == selected_nodo]
        rvn_filtered = rvn[
            rvn['COD_ZNJE'] == filtered_df[filtered_df['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[
                0]] if selected_liquidacion == 'Sell In' else rvn_so[
            rvn_so['COD_ZNJE'] == filtered_df[filtered_df['DES_ZNJE'] == selected_nodo]['COD_ZNJE'].unique()[0]]

    # Generar opciones actualizadas para el dropdown de 'Tipo de Descuento'
    tipo_descuento_options = [{'label': tipo, 'value': tipo} for tipo in filtered_df['TIPO_DESCUENTO'].unique()]

    # Generar opciones actualizadas para el dropdown de 'Año'
    year_options = [{'label': year, 'value': year} for year in rvn_filtered['YEAR'].unique()]

    # Filtrar maestro de ventas según el año seleccionado
    if selected_year:
        rvn_filtered = rvn_filtered[rvn_filtered['YEAR'] == selected_year]

    # Generar opciones actualizadas para el dropdown de 'Mes'
    month_options = [{'label': month, 'value': month} for month in rvn_filtered['MONTH'].unique()]

    # Retornar las opciones actualizadas
    return nodo_options, tipo_descuento_options, year_options, month_options, sell_in_class, sell_out_class