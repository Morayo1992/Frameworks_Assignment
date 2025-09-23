import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # possible files to look for
    possible_files = ["metadata.csv", "metadata_sample.csv"]

    path = None
    for file in possible_files:
        if os.path.exists(file):
            st.info(f"✅ Loaded data from `{file}`")
            path = file
            break

    if path is None:
        st.error("❌ No metadata file found. Please add either `metadata.csv` or `metadata_sample.csv` to the project folder.")
        return pd.DataFrame()

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
