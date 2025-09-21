import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

#import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Load the smaller CSV that exists in the repo
    df = pd.read_csv("metadata_sample.csv")
    return df

st.title("Frameworks Assignment App")

df = load_data()

st.write("### Preview of dataset")
st.dataframe(df.head(20))

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
