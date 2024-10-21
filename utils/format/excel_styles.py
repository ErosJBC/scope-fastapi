"""
A module for Excel styles in the engineering.loading.formatting package.
"""

import logging
from random import randint

import pandas as pd
from openpyxl.styles import Font, NamedStyle
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import PositiveInt

from utils.utils import get_excel_column_letter

logger: logging.Logger = logging.getLogger(__name__)


def apply_table_style(
    worksheet: Worksheet,
    num_rows: PositiveInt,
    num_cols: PositiveInt,
    display_name: str,
) -> None:
    """
    Apply a random table style to the worksheet.

    :param worksheet: The worksheet to apply the table style
    :type worksheet: Worksheet
    :param num_rows: The number of rows to apply the table style
    :type num_rows: PositiveInt
    :param num_cols: The number of columns to apply the table style
    :type num_cols: PositiveInt
    :param display_name: The name of the display to apply the table style
    :type display_name: str
    :return: None
    :rtype: NoneType
    """
    table_range: str = f"A1:{get_excel_column_letter(num_cols)}{num_rows + 1}"
    random_color_number: PositiveInt = randint(8, 14)
    random_color_name: str = f"TableStyleLight{random_color_number}"
    table: Table = Table(displayName=display_name, ref=table_range)
    table_style_info: TableStyleInfo = TableStyleInfo(
        name=random_color_name,
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=True,
    )
    table.tableStyleInfo = table_style_info
    worksheet.add_table(table)
    logger.info("Table created successfully")


def add_named_styles(worksheet: Worksheet) -> None:
    """
    Add named styles to the workbook if they do not already exist.

    :param worksheet: The worksheet whose parent workbook to check for named
     styles
    :type worksheet: Worksheet
    :return: None
    :rtype: NoneType
    """
    styles: list[NamedStyle] = [
        NamedStyle(name="percentage_style", number_format="0.00%"),
        NamedStyle(name="currency_style", number_format="$#,##0.00"),
        NamedStyle(name="integer_style", number_format="0"),
        NamedStyle(name="text_style", number_format="@"),
        NamedStyle(name="decimal_style", number_format="#,##0.00"),
    ]
    existing_style_names: set[str] = set(worksheet.parent.named_styles)
    for style in styles:
        if style.name not in existing_style_names:
            try:
                worksheet.parent.add_named_style(style)
                logging.info(f"Style {style.name} added successfully.")
            except ValueError as e:
                logging.warning(f"Could not add style {style.name}: {e}")
        else:
            logging.info(f"Style {style.name} already exists.")


def get_style_for_column(
    column_name: str,
    dataframe: pd.DataFrame,
) -> str:
    """
    Determine the style to apply to a column based on its name and data type.

    :param column_name: The name of the column
    :type column_name: str
    :param dataframe: The dataframe containing the column to check its data type
    :type dataframe: pd.DataFrame
    :return: The name of the style to apply
    :rtype: str
    """
    if column_name.startswith("DESCUENTO"):
        return "percentage_style"
    elif column_name.startswith("PRECIO"):
        return "currency_style"
    elif column_name.startswith("COD_"):
        # TODO: Add exception for COD_PAIS as it should be TEXT
        if column_name == "COD_PAIS":
            return "text_style"
        return "integer_style"
    elif pd.api.types.is_numeric_dtype(dataframe[column_name]):
        return "decimal_style"
    else:
        return "text_style"


def apply_style_to_column(
    worksheet: Worksheet,
    column_letter: str,
    style_name: str,
    num_rows: PositiveInt,
) -> None:
    """
    Apply a specified style to all cells in a column.

    :param worksheet: The worksheet containing the column
    :type worksheet: Worksheet
    :param column_letter: The letter of the column to style
    :type column_letter: str
    :param style_name: The name of the style to apply
    :type style_name: str
    :param num_rows: The number of rows to apply the style to
    :type num_rows: int
    :return: None
    :rtype: NoneType
    """
    for cell in worksheet[column_letter][0 : num_rows + 1]:
        cell.style = style_name


def apply_column_styles(
    worksheet: Worksheet,
    num_rows: PositiveInt,
    dataframe: pd.DataFrame,
) -> None:
    """
    Apply styles to columns based on their content.

    :param worksheet: The worksheet to apply styles on its columns
    :type worksheet: Worksheet
    :param num_rows: The number of rows to consider the style
    :type num_rows: PositiveInt
    :param dataframe: The dataframe to analyze its columns
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    add_named_styles(worksheet)
    column_letter: str
    column_name: str
    style_name: str
    for col in worksheet.iter_cols(min_row=1, max_row=num_rows + 1):
        column_letter = col[0].column_letter
        column_name = worksheet[f"{column_letter}1"].value
        style_name = get_style_for_column(column_name, dataframe)
        apply_style_to_column(worksheet, column_letter, style_name, num_rows)
    logging.info("Column styles added to the worksheet: %s", worksheet.title)


def adjust_column_widths(worksheet: Worksheet) -> None:
    """
    Adjust the width of the columns in the worksheet.

    :param worksheet: The worksheet to adjust its column widths
    :type worksheet: Worksheet
    :return: None
    :rtype: NoneType
    """
    max_length: int
    column: str
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if cell.value is not None:
                    if isinstance(cell.value, str):
                        max_length = max(max_length, len(cell.value))
                    else:
                        max_length = max(max_length, len(str(cell.value)))
            except TypeError:
                continue
        adjusted_width = max_length + 5
        worksheet.column_dimensions[column].width = adjusted_width
    logger.info("Adjusted width to worksheet: %s", worksheet)


def format_header(worksheet: Worksheet) -> None:
    """
    Format the header row of the worksheet.

    :param worksheet: The worksheet to format its header
    :type worksheet: Worksheet
    :return: None
    :rtype: NoneType
    """
    header_font: Font = Font(
        color="FFFFFF",
        bold=True,
    )
    for cell in worksheet[1]:
        cell.font = header_font
    logger.info("Formatted header for worksheet: %s", worksheet)
