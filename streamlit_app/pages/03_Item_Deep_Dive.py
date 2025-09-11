
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Item Deep Dive", page_icon="🧪", layout="wide")
st.title("🧪 Item Deep Dive")

df = load_data()
fdf = apply_sidebar_filters(df)

name_col = "Item Name Cleaned" if "Item Name Cleaned" in fdf.columns else ("Item Name" if "Item Name" in fdf.columns else None)
value_col = "Total Bcy" if "Total Bcy" in fdf.columns else ("Sub Total Bcy" if "Sub Total Bcy" in fdf.columns else None)

if name_col:
    items = ["— Select —"] + sorted([x for x in fdf[name_col].dropna().unique().tolist() if x != "nan"])
    sel = st.selectbox("Pick an item", items, index=0)
    if sel != "— Select —":
        sdf = fdf[fdf[name_col] == sel].copy()
        st.subheader("Stats")
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("Occurrences", len(sdf))
        if value_col:
            with c2: st.metric("Total Spend", f"{sdf[value_col].sum(skipna=True):,.2f}")
        if "Quantity" in sdf.columns:
            with c3: st.metric("Total Qty", f"{sdf['Quantity'].sum(skipna=True):,.0f}")
        if "Unit Price" in sdf.columns:
            with c4: st.metric("Median Unit Price", f"{sdf['Unit Price'].median(skipna=True):,.2f}")
        st.markdown("---")
        # Distribution of Unit Price
        if "Unit Price" in sdf.columns and sdf["Unit Price"].notna().any():
            st.subheader("Unit Price Distribution")
            hist = px.histogram(sdf, x="Unit Price", nbins=30, marginal="box")
            st.plotly_chart(hist, use_container_width=True)
        # Scatter of Spend vs Qty
        if value_col and "Quantity" in sdf.columns:
            st.subheader("Spend vs Quantity")
            sc = px.scatter(sdf, x="Quantity", y=value_col, hover_data=["Purchase Order ID"] if "Purchase Order ID" in sdf.columns else None, trendline="ols")
            st.plotly_chart(sc, use_container_width=True)
        st.subheader("Raw Records")
        st.dataframe(sdf, use_container_width=True, height=420)
else:
    st.info("Item name column not found.")
