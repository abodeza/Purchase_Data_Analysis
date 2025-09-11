import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_sidebar_filters, get_spend_col

st.set_page_config(page_title="Entity Dashboards", page_icon="🏷️", layout="wide")
st.title("🏷️ Entity Dashboards")

df = load_data()
fdf = apply_sidebar_filters(df)
spend_col = get_spend_col(fdf)

entities = [c for c in ["Account ID", "Currency Code", "Tax ID"] if c in fdf.columns]
if not entities:
    st.info("No entity columns found.")
else:
    for ent in entities:
        st.markdown("---")
        st.subheader(f"{ent} Overview")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Unique", fdf[ent].nunique(dropna=True))
        if spend_col:
            with c2: st.metric("Total Spend", f"{fdf[spend_col].sum(skipna=True):,.2f}")
        with c3: st.metric("Rows", len(fdf))

        # Top by spend/count
        if spend_col:
            agg = fdf.groupby(ent, dropna=True)[spend_col].sum().reset_index().sort_values(spend_col, ascending=False).head(25)
            bar = px.bar(agg, x=ent, y=spend_col, title=f"Top {ent} by Spend")
            st.plotly_chart(bar, use_container_width=True)
        cnt = fdf[ent].value_counts(dropna=True).reset_index().rename(columns={"index": ent, ent: "Count"})
        st.dataframe(cnt, use_container_width=True, height=320)