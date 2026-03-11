import tools
from langchain.agents import create_agent
from llm import get_llm

def create_data_agent(df):

    tools.GLOBAL_DF = df

    llm = get_llm()

    tool_list = [
        tools.dataset_summary,
        tools.total_sales,
        tools.total_profit,
        tools.sales_by_category,
        tools.run_pandas_code
    ]

    agent = create_agent(
        model=llm,
        tools=tool_list,
        system_prompt=f"""
        You are a professional AI Data Analyst.
        The dataset is stored in a pandas DataFrame called df.
        The dataset columns can be accessed from df.columns.
        Guidelines:
        - Use tools to answer questions.
        - For charts, graphs, comparisons, trends, or visualizations ALWAYS use the run_pandas_code tool.
        - Generate Python code using pandas and matplotlib.
        - The dataframe name must always be df.
        - Do not explain charts in text.""")

    return agent