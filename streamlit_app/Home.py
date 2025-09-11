
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, kpi_total_spend, kpi_unique, apply_sidebar_filters, download_button

st.set_page_config(page_title="Purchasing Analytics", page_icon="📦", layout="wide")

st.title("📦 Purchasing Analytics — Overview")
st.caption("A quick, interactive overview of your purchase order items. | [GitHub Repo](https://github.com/abodeza/Purchase_Data_Analysis/tree/main)")

df = load_data()
fdf = apply_sidebar_filters(df)

spend = kpi_total_spend(fdf)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Spend", f"{spend:,.2f}")
with c2:
    st.metric("Unique Items", kpi_unique(fdf, "Item ID") if "Item ID" in fdf.columns else fdf.shape[0])
with c3:
    st.metric("Unique POs", kpi_unique(fdf, "Purchase Order ID"))
with c4:
    st.metric("Avg Unit Price", f"{fdf['Unit Price'].mean(skipna=True):,.2f}" if "Unit Price" in fdf.columns else "—")

st.markdown("---")
value_col = "Total Bcy" if "Total Bcy" in fdf.columns else ("Sub Total Bcy" if "Sub Total Bcy" in fdf.columns else None)
if value_col and "Category" in fdf.columns and "Subcategory" in fdf.columns:
    st.subheader("Category Breakdown (Treemap)")
    treemap = px.treemap(fdf, path=["Category", "Subcategory"], values=value_col, hover_data=["Item Name Cleaned"] if "Item Name Cleaned" in fdf.columns else None)
    st.plotly_chart(treemap, use_container_width=True)

if value_col and "Item Name Cleaned" in fdf.columns:
    st.subheader("Top Items by Spend")
    top = fdf.groupby("Item Name Cleaned", dropna=True)[value_col].sum().sort_values(ascending=False).head(20).reset_index()
    bar = px.bar(top, x=value_col, y="Item Name Cleaned", orientation="h")
    st.plotly_chart(bar, use_container_width=True)

st.markdown("---")
st.subheader("Explore Filtered Data")
st.dataframe(fdf, use_container_width=True, height=420)
download_button(fdf)

st.markdown("---")
with st.expander("About & Contact"):
    st.markdown(
        "- **Author:** Abdullah Alzahrani  \n"
        "- **Email:** [abdullah.alzahrani.p@gmail.com](mailto:abdullah.alzahrani.p@gmail.com)  \n"
        "- **GitHub:** [@abodeza](https://github.com/abodeza)  \n"
        "- **LinkedIn:** [a-a-alzahrani](https://linkedin.com/in/a-a-alzahrani)"
    )
