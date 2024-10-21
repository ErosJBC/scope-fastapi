import pandas as pd

def filter_binnacle(binnacle: pd.DataFrame, sales: pd.DataFrame, selected_liquidation: str) -> pd.DataFrame:
    """
    Filter the binnacle dataframe based on the selected 'Nodo'

    :param binnacle: The binnacle dataframe
    :type binnacle: pd.DataFrame
    :param sales: The sales dataframe
    :type sales: pd.DataFrame
    :param selected_liquidation: The selected liquidation
    :type selected_liquidation: str
    :return: The filtered binnacle dataframe
    :rtype: pd.DataFrame
    """
    filtered_df: pd.DataFrame = binnacle[(binnacle['SI/SO'] == selected_liquidation) & (binnacle['COD_ZNJE'].isin(sales['COD_ZNJE'].unique()))]
    return filtered_df

def filter_sales(sales: pd.DataFrame, sellout: pd.DataFrame, filtered_binnacle: pd.DataFrame, selected_liquidation: str) -> pd.DataFrame:
    """
    Filter the sales dataframe based on the selected 'Nodo'

    :param sales: The sales dataframe
    :type sales: pd.DataFrame
    :param sellout: The sellout dataframe
    :type sellout: pd.DataFrame
    :param filtered_binnacle: The filtered binnacle dataframe
    :type filtered_binnacle: pd.DataFrame
    :param selected_liquidation: The selected liquidation
    :type selected_liquidation: str
    :return: The filtered sales dataframe
    :rtype: pd.DataFrame
    """
    filtered_df: pd.DataFrame
    if selected_liquidation == 'Sell Out':
        filtered_df = sales[sales['COD_ZNJE'].isin(filtered_binnacle['COD_ZNJE'].unique())]
    else:
        filtered_df = sellout[sellout['COD_ZNJE'].isin(filtered_binnacle['COD_ZNJE'].unique())]
    return filtered_df
