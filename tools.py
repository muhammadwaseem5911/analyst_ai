from langchain_core.tools import tool
import matplotlib.pyplot as plt
import pandas as pd

GLOBAL_DF = None

@tool
def dataset_summary() -> str:
    """Provides statistical summary of dataset"""
    if GLOBAL_DF is None:
        return "Dataset not loaded."
    return GLOBAL_DF.describe().to_string()


@tool
def total_sales() -> str:
    """Returns total sales value"""
    if GLOBAL_DF is None:
        return "Dataset not loaded."
    return f"Total Sales: {GLOBAL_DF['Sales'].sum()}"


@tool
def total_profit() -> str:
    """Returns total profit value"""
    if GLOBAL_DF is None:
        return "Dataset not loaded."
    return f"Total Profit: {GLOBAL_DF['Profit'].sum()}"


@tool
def sales_by_category() -> str:
    """Returns sales grouped by category"""
    if GLOBAL_DF is None:
        return "Dataset not loaded."
    return GLOBAL_DF.groupby("Category")["Sales"].sum().to_string()

# @tool
# def create_chart(x_column: str, y_column: str, chart_type: str = "bar") -> str:
#     """ Use this tool when you see there comparison between two feature and try to make perfect chart also Use scatter chart for relationships between two numeric columns.
#     Use bar chart for comparisons between Categories.
#     Use line chart for trends over time.
#     Args:
#         x_column: column for X axis
#         y_column: column for Y axis
#         chart_type: bar, line, or scatter
#     """

#     df = GLOBAL_DF

#     if chart_type == "bar":
#         data = df.groupby(x_column)[y_column].sum()

#         fig, ax = plt.subplots()
#         data.plot(kind="bar", ax=ax)

#     elif chart_type == "line":
#         data = df.groupby(x_column)[y_column].sum()

#         fig, ax = plt.subplots()
#         data.plot(kind="line", ax=ax)

#     elif chart_type == "scatter":

#         fig, ax = plt.subplots()
#         ax.scatter(df[x_column], df[y_column])

#     else:
#         return "Unsupported chart type"

#     file_name = "chart.png"
#     fig.savefig(file_name)

#     return file_name

@tool
def run_pandas_code(code: str):
    """Execute pandas code on dataframe df and return chart and code."""

    df = GLOBAL_DF
    code = code.replace("plt.show()", "")
    local_vars = {
        "df": df,
        "plt": plt,
        "pd": pd
        }
    try:
        plt.clf()
        plt.figure()

        exec(code, {}, local_vars)

        fig = plt.gcf()

        return {
            "code": code,
            "figure": fig
        }

    except Exception as e:
        return f"Error executing code: {str(e)}"