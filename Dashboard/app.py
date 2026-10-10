import pandas as pd
import streamlit as st
data = pd.read_excel("Data/european bank.xlsx")
data["ActivityPoints"] = data["IsActiveMember"]
data["ProductPoints"] = data["NumOfProducts"].apply(
    lambda x: 1 if x >= 2 else 0)
data["RelationshipScore"] = data["ActivityPoints"] + data["ProductPoints"]
data["RelationshipScore"] = data["ActivityPoints"] + data["ProductPoints"]
relationship_churn = data.groupby("RelationshipScore")["Exited"].mean() * 100
relationship_churn = relationship_churn.round(2)
relationship_churn = relationship_churn.rename("Churn Rate (%)")
churn_rate = data["Exited"].mean() * 100
total_customers = data.shape[0]
churned_customers = data["Exited"].value_counts()[1]
st.title("Customer Retention Dashboard")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
with col2:
    st.metric("Total Customers", total_customers)
with col3:
    st.metric("Churned Customers", churned_customers)
geography_churn = data.groupby("Geography")["Exited"].mean() * 100
geography_churn = geography_churn.round(2)
geography_churn = geography_churn.rename("Churn Rate (%)")
st.subheader("Churn Rate by Geography")
st.bar_chart(geography_churn,y_label="Churn Rate (%)")
st.write(geography_churn)
st.write(
    "Key insight: Germany had a substantially higher observed churn rate "
    "(32.44%) than France (16.15%) and Spain (16.67%). This indicates an "
    "association between geography and observed churn, but does not establish "
    "that geography causes churn. The bank should investigate customer "
    "characteristics and engagement patterns within the German segment further.")
activity_churn = data.groupby("IsActiveMember")["Exited"].mean() * 100
activity_churn = activity_churn.round(2)
st.subheader("Churn Rate by Customer Activity")
st.bar_chart(activity_churn, y_label="Churn Rate (%)")
activity_summary = pd.DataFrame({
    "Customer Activity": ["Inactive", "Active"],
    "Churn Rate (%)": [ activity_churn[0],
        activity_churn[1]]})
st.dataframe(activity_summary, hide_index=True)
st.write(
    "Key insight: Active customers had a lower observed churn rate "
    "(14.27%) than inactive customers (26.85%), suggesting an association "
    "between customer engagement and retention. This does not establish causation.")
st.subheader("Churn Rate by Relationship Score")
st.bar_chart(relationship_churn,y_label="Churn Rate (%)")
relationship_summary = pd.DataFrame({
    "Score": ["Score 0", "Score 1", "Score 2"],
    "Customer Profile": [
        "Inactive + 1 product",
        "Active + 1 product OR Inactive + 2+ products",
        "Active + 2+ products"],
    "Churn Rate (%)": [
        relationship_churn[0],
        relationship_churn[1],
        relationship_churn[2]]})
st.dataframe(relationship_summary, hide_index=True)
average_balance = data["Balance"].mean()
data["HighBalance"] = data["Balance"] > average_balance
high_balance_inactive = data[
    (data["HighBalance"] == True) &
    (data["IsActiveMember"] == 0)]
high_balance_inactive_churn = high_balance_inactive["Exited"].mean() * 100
st.write(
    "Key insight: Relationship Score combines customer activity and product depth "
    "into a simple descriptive measure. Customers with Score 2 had the lowest "
    "observed churn rate (9.66%), while Score 0 had the highest (36.65%). "
    "This suggests an association between stronger customer engagement/product "
    "relationships and lower observed churn, but the analysis does not establish causation.")
st.subheader("High-Balance Disengagement")
col1, col2 = st.columns(2)
with col1:
    st.metric("High-Balance Inactive Customers", len(high_balance_inactive))
with col2:st.metric("Observed Churn Rate", f"{high_balance_inactive_churn:.2f}%")
germany_score0_over40 = data[
    (data["Geography"] == "Germany") &
    (data["RelationshipScore"] == 0) &
    (data["Age"] > 40)]
st.subheader("High-Risk Customer Segment")
st.markdown("**Segment criteria:**")
st.markdown(
    "**Germany**  |  **Relationship Score 0**  |  **Age > 40**")
germany_score0_over40_churn = germany_score0_over40["Exited"].mean() * 100
col1, col2 = st.columns(2)
with col1:
    st.metric("High-Risk Customers", len(germany_score0_over40))
with col2:
    st.metric("Observed Churn Rate", f"{germany_score0_over40_churn:.2f}%")
product_churn = data.groupby("NumOfProducts")["Exited"].mean() * 100
product_churn = data.groupby("NumOfProducts")["Exited"].mean() * 100
product_churn = product_churn.round(2)
st.subheader("Churn Rate by Number of Products")
st.bar_chart(product_churn,y_label="Churn Rate (%)")
product_counts = data["NumOfProducts"].value_counts().sort_index()
product_summary = pd.DataFrame({
    "Customers": product_counts,
    "Churn Rate (%)": product_churn})
product_summary.index.name = "Number of Products"
st.dataframe(product_summary)
st.write(
    "Key insight: Customers with 2 products had the lowest observed churn rate (7.58%). "
    "The 3- and 4-product groups showed much higher observed churn, but these groups "
    "are relatively small and the observed relationship indicates an association, not causation.")