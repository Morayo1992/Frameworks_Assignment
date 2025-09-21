import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

# Year filter
years = st.slider("Select year range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
filtered = df[df['year'].between(years[0], years[1])]

# Publications by Year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
st.pyplot(fig)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax)
st.pyplot(fig)

# Word Cloud
st.subheader("Word Cloud of Titles")
text = " ".join(str(title) for title in filtered['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Show sample data
st.subheader("Sample Data")
st.write(filtered[['title', 'journal', 'publish_time']].head(10))
