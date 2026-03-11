import os
from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import pandas as pd
from tool import clean_data
from tool import analysis
from tool import plot_sales_by_category
from agenti import create_data_agent

st.set_page_config(page_title="AI Data Analyst Assistant")
st.title("📊 AI Data Analyst Assistant")
uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["xlsx", "csv"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    st.subheader("Dataset Info")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])
    
    df, report = clean_data(df)
    st.subheader("🧹 Data Cleaning Report")
    st.write("Missing Values:", report["missing_values"])
    st.write("Duplicates Removed:", report["duplicates"])
    
    summary = analysis(df)

    st.subheader("📈 Key Metrics")
    st.write("Total Sales:", round(summary["total_sales"], 2))
    st.write("Total Profit:", round(summary["total_profit"], 2))
    st.write("Average Sales:", round(summary["avg_sales"], 2))
    
    st.subheader("📊 Sales by Category")
    fig = plot_sales_by_category(df)
    st.pyplot(fig)

    agent = create_data_agent(df)

    user_question = st.text_input("Ask AI Analyst")

    if user_question:

        response = agent.invoke(
        {"messages": [{"role": "user", "content": user_question}]})

        st.write("🤖 AI Insight:")

        messages = response["messages"]

        chart_found = False

        for msg in messages:

            if isinstance(msg.content, dict):

                result = msg.content

                if "code" in result:
                    st.subheader("🧠 Generated Code")
                    st.code(result["code"], language="python")

                if "figure" in result:
                    st.subheader("📊 Chart")
                    st.pyplot(result["figure"])
                    chart_found = True

            else:
             if not chart_found:
                st.write(msg.content)