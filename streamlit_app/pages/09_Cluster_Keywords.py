import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
from io import BytesIO
from utils import load_data, apply_sidebar_filters

st.set_page_config(page_title="Cluster Keywords", page_icon="🧩", layout="wide")
st.title("🧩 Cluster Keywords & Word Clouds")
st.caption("⚠️ Note: Arabic text may not be visualized well in the word clouds.")

df = load_data()
fdf = apply_sidebar_filters(df)

name_col = "Item Name Cleaned" if "Item Name Cleaned" in fdf.columns else ("Item Name" if "Item Name" in fdf.columns else None)
group_col = None
if "Subcategory" in fdf.columns:
    group_col = "Subcategory"
elif "Category" in fdf.columns:
    group_col = "Category"

if not name_col or not group_col:
    st.info("Need item names and a grouping column (Category/Subcategory).")
else:
    groups = sorted([g for g in fdf[group_col].dropna().unique().tolist() if str(g).strip() != ""])
    sel = st.multiselect(f"Pick {group_col}(s)", groups, default=groups[:6])
    n_top = st.slider("Top N keywords (TF‑IDF)", 5, 40, 15)

    for g in sel:
        sub = fdf[fdf[group_col] == g][name_col].dropna().astype(str).tolist()
        if not sub:
            continue
        vect = TfidfVectorizer(max_features=5000, ngram_range=(1,2), min_df=1)
        X = vect.fit_transform(sub)
        tfidf_sum = X.sum(axis=0).A1
        feats = vect.get_feature_names_out()
        top_idx = tfidf_sum.argsort()[::-1][:n_top]
        top_terms = [(feats[i], tfidf_sum[i]) for i in top_idx]
        st.markdown(f"### {group_col}: **{g}** — Top {n_top} terms")

        st.dataframe(pd.DataFrame(top_terms, columns=["term","score"]), use_container_width=True, height=220)

        freq = {t: float(s) for t, s in top_terms}
        wc = WordCloud(width=800, height=300, background_color="black", colormap="viridis").generate_from_frequencies(freq)
        buf = BytesIO()
        wc.to_image().save(buf, format="PNG")
        st.image(buf.getvalue())