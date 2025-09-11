
import pandas as pd
import streamlit as st
from pathlib import Path

HERE = Path(__file__).parent   # streamlit_app/
DEFAULT_DATA_PATH = HERE / "processed-purchase-order-items.xlsx"

@st.cache_data(show_spinner=False)
def load_data(path: str | None = None) -> pd.DataFrame:
    candidates = []
    if path:
        candidates.append(Path(path))
    candidates.append(Path(DEFAULT_DATA_PATH))
    for p in candidates:
        if p.exists():
            df = pd.read_excel(p)
            return _postprocess(df)
    st.stop()

def _postprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    spend_cols = ["Total Bcy", "Sub Total Bcy"]
    qty_col = "Quantity"
    spend = None
    for c in spend_cols:
        if c in df.columns:
            spend = c
            break
    if spend and qty_col in df.columns:
        with pd.option_context("mode.use_inf_as_na", True):
            df["Unit Price"] = df.apply(lambda r: (r[spend] / r[qty_col]) if pd.notna(r[spend]) and pd.notna(r[qty_col]) and r[qty_col] not in (0, None) else pd.NA, axis=1)
    for c in ["Quantity", "Total Bcy", "Sub Total Bcy", "Unit Price"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["Item Name", "Item Name Cleaned", "Category", "Subcategory", "Currency Code"]:
        if c in df.columns:
            df[c] = df[c].astype("string").str.strip()
    return df

def kpi_total_spend(df: pd.DataFrame) -> float:
    for c in ["Total Bcy", "Sub Total Bcy"]:
        if c in df.columns:
            return float(pd.to_numeric(df[c], errors="coerce").sum(skipna=True))
    return float("nan")

def kpi_unique(df: pd.DataFrame, col: str) -> int:
    return int(df[col].nunique(dropna=True)) if col in df.columns else 0

def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    st.sidebar.header("Filters")
    if "Category" in out.columns:
        cats = ["All"] + sorted([x for x in out["Category"].dropna().unique().tolist() if x != "nan"])
        sel_cat = st.sidebar.selectbox("Category", cats, index=0)
        if sel_cat != "All":
            out = out[out["Category"] == sel_cat]
    if "Subcategory" in out.columns:
        subs = ["All"] + sorted([x for x in out["Subcategory"].dropna().unique().tolist() if x != "nan"])
        sel_sub = st.sidebar.selectbox("Subcategory", subs, index=0)
        if sel_sub != "All":
            out = out[out["Subcategory"] == sel_sub]
    for name_col in ["Item Name Cleaned", "Item Name"]:
        if name_col in out.columns:
            q = st.sidebar.text_input("Search item name")
            if q:
                out = out[out[name_col].str.contains(q, case=False, na=False)]
            break
    if "Quantity" in out.columns:
        qmin, qmax = float(out["Quantity"].min(skipna=True) or 0), float(out["Quantity"].max(skipna=True) or 0)
        if qmax > qmin:
            r = st.sidebar.slider("Quantity range", qmin, qmax, (qmin, qmax))
            out = out[(out["Quantity"] >= r[0]) & (out["Quantity"] <= r[1])]
    spend_col = None
    for c in ["Total Bcy", "Sub Total Bcy"]:
        if c in out.columns:
            spend_col = c
            break
    if spend_col:
        smin, smax = float(out[spend_col].min(skipna=True) or 0), float(out[spend_col].max(skipna=True) or 0)
        if smax > smin:
            r = st.sidebar.slider(f"{spend_col} range", smin, smax, (smin, smax))
            out = out[(out[spend_col] >= r[0]) & (out[spend_col] <= r[1])]
    return out

def download_button(df: pd.DataFrame, label: str = "Download filtered CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label, data=csv, file_name="filtered_export.csv", mime="text/csv")


def get_spend_col(df: pd.DataFrame) -> str | None:
    for c in ["Total Bcy", "Sub Total Bcy"]:
        if c in df.columns:
            return c
    return None

def is_unknown_category(x) -> bool:
    if pd.isna(x):
        return True
    s = str(x).strip().lower()
    return s == "Unknown / Noise"


def filter_unknown(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Category"].apply(is_unknown_category)]

def log_toggle(label: str, default: bool = False) -> bool:
    return st.checkbox(label, value=default, help="Switch the axis/metric to log scale for skewed distributions.")
