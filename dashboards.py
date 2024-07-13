import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Add the title at the top of the page
st.markdown("<h1 style='text-align: center; color: #007bff;'>Sales Dashboard</h1>", unsafe_allow_html=True)

# Answering questions with a monthly view:
# 01 Revenue by unit
# 02 Most sold product type, contribution by branch
# 03 Performance of payment methods
# 04 How are the branch ratings?

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Filter for January 2024
df_filtered = df[df["Month"] == "2024-1"]

# Replace city names
city_mapping = {
    "Yangon": "Bombay",
    "Mandalay": "Bangalore",
    "Naypyitaw": "Kolkata"
}
df_filtered["City"] = df_filtered["City"].map(city_mapping)

# Function to create and display a chart with a specific width
def display_chart(fig, title):
    fig.update_layout(
        title=title,
        width=600,  # Adjust this value to make charts narrower or wider
        height=400
    )
    st.plotly_chart(fig, use_container_width=False)

# 01 Revenue by unit
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City")
display_chart(fig_date, "Daily Revenue")

# 02 Most sold product type, contribution by branch
fig_prod = px.bar(df_filtered, x="Total", y="Product line", color="City", orientation="h")
display_chart(fig_prod, "Revenue by Product Type")

# Revenue by branch
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total")
display_chart(fig_city, "Revenue by Branch")

# 03 Performance of payment methods
fig_kind = px.pie(df_filtered, values="Total", names="Payment")
display_chart(fig_kind, "Revenue by Payment Type")

# 04 How are the branch ratings?
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City")
display_chart(fig_rating, "Ratings")
