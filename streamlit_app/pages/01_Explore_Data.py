
import streamlit as st
import pandas as pd
from utils import load_data, apply_sidebar_filters, download_button

st.set_page_config(page_title="Explore Data", page_icon="🔎", layout="wide")
st.title("🔎 Explore Data")

df = load_data()
fdf = apply_sidebar_filters(df)

st.subheader("Data Browser")
st.dataframe(fdf, use_container_width=True, height=560)
download_button(fdf)

st.markdown("---")
st.subheader("Quick Pivots")
left, right = st.columns(2)
with left:
    group_candidates = [c for c in fdf.columns if fdf[c].dtype == "object"]
    if len(group_candidates) == 0:
        group_candidates = [c for c in fdf.columns]
    group_col = st.selectbox("Group by", group_candidates, index=0)
with right:
    value_candidates = [c for c in ["Total Bcy", "Sub Total Bcy", "Quantity", "Unit Price"] if c in fdf.columns]
    value_col = st.selectbox("Aggregate value", value_candidates, index=0 if value_candidates else None)

if group_col and value_col:
    agg = fdf.groupby(group_col, dropna=True)[value_col].sum().reset_index().sort_values(value_col, ascending=False)
    st.dataframe(agg, use_container_width=True, height=420)
