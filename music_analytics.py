import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Music Streaming Analytics", page_icon="🎵", layout="wide")

st.title("🎵 Music Streaming Analytics & Insights")
st.caption("Interactive business-intelligence dashboard built from a Spotify-style tracks dataset.")

@st.cache_data
def read_csv(source):
    return pd.read_csv(source)

local_dataset = Path(__file__).with_name("dataset.csv")
uploaded = st.sidebar.file_uploader("Upload another CSV (optional)", type=["csv"])
if uploaded is not None:
    df = read_csv(uploaded)
else:
    if not local_dataset.exists():
        st.error("dataset.csv is missing. Upload the dataset from the sidebar.")
        st.stop()
    df = read_csv(local_dataset)

df = df.drop(columns=["Unnamed: 0"], errors="ignore")
df.columns = [str(c).strip() for c in df.columns]

def col(name):
    return name if name in df.columns else None

track_col, artist_col, genre_col, pop_col = col("track_name"), col("artists"), col("track_genre"), col("popularity")
dance_col, energy_col = col("danceability"), col("energy")
valence_col, tempo_col, duration_col = col("valence"), col("tempo"), col("duration_ms")

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🎵 Tracks", f"{len(df):,}")
c2.metric("🎤 Artists", f"{df[artist_col].nunique():,}" if artist_col else "N/A")
c3.metric("🎼 Genres", f"{df[genre_col].nunique():,}" if genre_col else "N/A")
c4.metric("⭐ Avg Popularity", f"{df[pop_col].mean():.1f}" if pop_col else "N/A")
c5.metric("⏱️ Avg Duration", f"{df[duration_col].mean()/60000:.2f} min" if duration_col else "N/A")

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🎤 Artists & Genres", "🔎 Explorer"])

with tab1:
    if pop_col:
        st.subheader("Popularity Distribution")
        fig, ax = plt.subplots()
        ax.hist(df[pop_col].dropna(), bins=20)
        ax.set_xlabel("Popularity")
        ax.set_ylabel("Tracks")
        ax.set_title("Track Popularity Distribution")
        st.pyplot(fig)

    if genre_col and pop_col:
        st.subheader("Top 15 Genres by Average Popularity")
        g = df.groupby(genre_col)[pop_col].mean().sort_values(ascending=False).head(15)
        st.bar_chart(g)

    if dance_col and energy_col:
        st.subheader("Danceability vs Energy")
        sample = df[[dance_col, energy_col]].dropna()
        if len(sample) > 5000:
            sample = sample.sample(5000, random_state=42)
        fig, ax = plt.subplots()
        ax.scatter(sample[dance_col], sample[energy_col], alpha=0.25)
        ax.set_xlabel("Danceability")
        ax.set_ylabel("Energy")
        ax.set_title("Audio Feature Relationship")
        st.pyplot(fig)

with tab2:
    if artist_col and pop_col:
        st.subheader("Artists with at Least 3 Tracks")
        a = (df.groupby(artist_col)
             .agg(average_popularity=(pop_col, "mean"), tracks=(pop_col, "count"))
             .query("tracks >= 3")
             .sort_values("average_popularity", ascending=False)
             .head(20))
        st.dataframe(a, use_container_width=True)

        st.subheader("Artists with the Most Tracks")
        st.bar_chart(df[artist_col].value_counts().head(15))

    if genre_col:
        st.subheader("Genres with the Most Tracks")
        st.bar_chart(df[genre_col].value_counts().head(20))

with tab3:
    st.subheader("Filter Dataset")
    filtered = df.copy()
    if genre_col:
        genres = sorted(filtered[genre_col].dropna().astype(str).unique())
        selected = st.multiselect("Genre", genres)
        if selected:
            filtered = filtered[filtered[genre_col].astype(str).isin(selected)]
    if pop_col:
        pmin, pmax = float(df[pop_col].min()), float(df[pop_col].max())
        pr = st.slider("Popularity", pmin, pmax, (pmin, pmax))
        filtered = filtered[filtered[pop_col].between(*pr)]
    st.write(f"Showing **{len(filtered):,}** rows")
    st.dataframe(filtered.head(500), use_container_width=True)

st.divider()
st.subheader("💡 Dataset-Driven Insights")
insights = []
if pop_col:
    insights.append(f"The dataset contains {len(df):,} tracks and the average popularity score is {df[pop_col].mean():.1f}.")
if genre_col and pop_col:
    best = df.groupby(genre_col)[pop_col].mean().sort_values(ascending=False)
    insights.append(f"'{best.index[0]}' has the highest average popularity among genres in this dataset ({best.iloc[0]:.1f}).")
if artist_col:
    artist_counts = df[artist_col].value_counts()
    insights.append(f"'{artist_counts.index[0]}' is the most represented artist in the dataset with {artist_counts.iloc[0]} tracks.")
if pop_col and dance_col:
    corr = df[[pop_col, dance_col]].corr().iloc[0,1]
    insights.append(f"The popularity–danceability Pearson correlation is {corr:.2f}; this is an association, not proof of causation.")
for x in insights:
    st.write("• " + x)

st.caption("Analysis is descriptive and reflects this dataset's coverage and definitions.")
