import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("metadata.csv")
    except FileNotFoundError:
        df = pd.read_csv("metadata_sample.csv")  # fallback
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

    # Try reading the file safely
    try:
        df = pd.read_csv(path, low_memory=False)
    except pd.errors.EmptyDataError:
        st.error(f"{path} is empty or malformed.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading {path}: {e}")
        return pd.DataFrame()

    # Ensure important columns exist
    if "publish_time" in df.columns:
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
        df["year"] = df["publish_time"].dt.year
    else:
        df["year"] = pd.NA

    if "title" not in df.columns:
        df["title"] = ""
    if "journal" not in df.columns:
        df["journal"] = "Unknown"

    # Clean up text columns
    df["title"] = df["title"].astype(str).str.strip()
    df["journal"] = df["journal"].astype(str).str.strip().replace("", "Unknown")

    return df
