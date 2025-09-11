
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Category Explorer", page_icon="🧭", layout="wide")
st.title("🧭 Category & Subcategory Explorer")

df = load_data()
fdf = apply_sidebar_filters(df)

value_col = "Total Bcy" if "Total Bcy" in fdf.columns else ("Sub Total Bcy" if "Sub Total Bcy" in fdf.columns else None)

if value_col and "Category" in fdf.columns:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Sunburst (Category → Subcategory → Item)")
        path = ["Category"]
        if "Subcategory" in fdf.columns: path.append("Subcategory")
        if "Item Name Cleaned" in fdf.columns: path.append("Item Name Cleaned")
        fig = px.sunburst(fdf, path=path, values=value_col, maxdepth=3)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Category Share")
        cat = fdf.groupby("Category", dropna=True)[value_col].sum().reset_index()
        pie = px.pie(cat, names="Category", values=value_col, hole=0.4)
        st.plotly_chart(pie, use_container_width=True)

    st.markdown("---")
    st.subheader("Subcategory Details")
    if "Subcategory" in fdf.columns:
        sub = fdf.groupby(["Category","Subcategory"], dropna=True)[value_col].sum().reset_index()
        if "Quantity" in fdf.columns:
            q = fdf.groupby(["Category","Subcategory"], dropna=True)["Quantity"].sum().reset_index()
            sub = sub.merge(q, on=["Category","Subcategory"], how="left")
        sub = sub.sort_values(value_col, ascending=False)
        st.dataframe(sub, use_container_width=True, height=420)
else:
    st.info("Category/Subcategory or spend columns not found.")
