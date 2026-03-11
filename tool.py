import pandas as pd
def clean_data(df):

    report = {}
    report["missing_values"] = df.isnull().sum().sum()
    report["duplicates"] = df.duplicated().sum()
    df = df.drop_duplicates()
    df = df.fillna(method="ffill")
    return df, report
def analysis(df):

    summary = {
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
        "avg_sales": df["Sales"].mean()
    }

    return summary

import matplotlib.pyplot as plt

def plot_sales_by_category(df):

    category_sales = df.groupby("Category")["Sales"].sum()

    fig, ax = plt.subplots()
    category_sales.plot(kind="bar", ax=ax)

    return fig