
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Price & Quantity Analysis", page_icon="📊", layout="wide")
st.title("📊 Price & Quantity Analysis")

df = load_data()
fdf = apply_sidebar_filters(df)

value_col = "Total Bcy" if "Total Bcy" in fdf.columns else ("Sub Total Bcy" if "Sub Total Bcy" in fdf.columns else None)

# 2D density: Quantity vs Spend (counts), masking erroneous values
if value_col and "Quantity" in fdf.columns:
    st.subheader("Quantity vs Spend (2D density)")

    # --- mask erroneous values ---
    d = fdf[["Quantity", value_col]].copy()

    # coerce to numeric and scrub NaNs/Infs
    d["Quantity"] = pd.to_numeric(d["Quantity"], errors="coerce")
    d[value_col]  = pd.to_numeric(d[value_col],  errors="coerce")
    d.replace([np.inf, -np.inf], np.nan, inplace=True)
    d.dropna(inplace=True)

    # drop non-positives (zeros/negatives)
    d = d[(d["Quantity"] > 0) & (d[value_col] > 0)]

    if d.empty:
        st.info("No valid (Quantity > 0, Spend > 0) rows to plot after masking.")
    else:
        # pick binning
        nbinsx, nbinsy = 60, 60

        # compute counts just to set a sensible color cap (avoid dark-blue washout)
        hx, xedges = np.histogram(d["Quantity"].to_numpy(), bins=nbinsx)
        hy, yedges = np.histogram(d[value_col].to_numpy(),  bins=nbinsy)
        H, _, _ = np.histogram2d(
            d["Quantity"].to_numpy(), d[value_col].to_numpy(),
            bins=[nbinsx, nbinsy]
        )
        cmax = float(np.percentile(H, 99)) if np.isfinite(H).any() else None
        # ensure cmax is usable
        rc = (0, cmax) if cmax and cmax > 0 else None

        # plain Plotly density heatmap
        heat = px.density_heatmap(
            d,
            x="Quantity",
            y=value_col,
            nbinsx=nbinsx,
            nbinsy=nbinsy,
            histfunc="count",
            color_continuous_scale="Viridis",
            range_color=rc,  # clip to 99th pct of counts
            labels={value_col: "Spend"}
        )

        st.plotly_chart(heat, use_container_width=True)
        st.caption(
            "Masked NaN/±∞ and non-positive values; color shows count per bin. "
            f"Color range clipped at 99th percentile (cmax≈{cmax:.0f}) to preserve contrast."
            if rc else
            "Masked NaN/±∞ and non-positive values; color shows count per bin."
        )

# Box plots by Category/Subcategory
group = None
if "Subcategory" in fdf.columns:
    group = "Subcategory"
elif "Category" in fdf.columns:
    group = "Category"

if group and value_col:
    st.subheader(f"Distribution of {value_col} by {group}")
    bx = px.box(fdf, x=group, y=value_col, points="outliers")
    st.plotly_chart(bx, use_container_width=True)

# Outlier detection on Unit Price (IQR)
if "Unit Price" in fdf.columns:
    st.subheader("Anomalies in Unit Price (IQR Rule)")
    g = fdf[["Unit Price"]].dropna()
    if len(g) > 0:
        q1, q3 = g["Unit Price"].quantile(0.25), g["Unit Price"].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        flagged = fdf[(fdf["Unit Price"] < lower) | (fdf["Unit Price"] > upper)]
        st.write(f"Outlier threshold: < {lower:,.2f} or > {upper:,.2f}")
        st.dataframe(flagged, use_container_width=True, height=420)
    else:
        st.info("Not enough data for Unit Price analysis.")
