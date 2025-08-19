import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import (
    get_connection, init_db, insert_transactions, load_transactions,
    add_category, get_categories, add_keyword, get_keywords, reapply_keywords
)

#uses streamlit to set title, icon, etc
st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

#initialize database with tables
init_db()

def categorize_transactions(df):
    #set every row to have a field uncategorized
    df["category"] = "Uncategorized"
    #get keyword dictionary
    keywords = get_keywords()

    #apply correct category
    for category, keyword_list in keywords.items():
        #category is invalid - uncategorized or keyword list is empty 
        if category == "Uncategorized" or not keyword_list:
            continue

        for idx, row in df.iterrows():
            #gets detail in each row (title of transaction)
            details = row["details"].lower().strip()
            #matches detail to a keyword if possible
            if details in keyword_list:
                df.at[idx, "category"] = category

    return df

def format_transactions(file):
    try:
        df = pd.read_csv(file)

        #in pandas can load in cols of csv file
        df.columns = [col.strip() for col in df.columns]

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        expected_cols = {"Date", "Details", "Amount", "Debit/Credit"}
        if not expected_cols.issubset(set(df.columns)):
            raise ValueError(f"Missing one or more required columns: {expected_cols}")

        df.rename(columns={
            "Date": "date",
            "Details": "details",
            "Amount": "amount",
            "Debit/Credit": "debit_or_credit",
        }, inplace=True)

        df["amount"] = df["amount"].str.replace(",", "").astype(float)
        df["date"] = pd.to_datetime(df["date"], format="%d %b %Y")

        return categorize_transactions(df)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def main():
    st.title("Simple Finance Dashboard")

    #automatically stored in state
    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

    if uploaded_file is not None:
        df = format_transactions(uploaded_file)

        if df is None:
            st.error("File processing failed - check CSV format")
            return
        
        insert_transactions(df)
        st.success("Transactions uploaded and saved")
        reapply_keywords()

    df = load_transactions()

    if df.empty:
        st.info("No transactions available yet.")
        return 
        
    #add transactions manually (user adds)
    with st.expander("Add Transaction Manually"):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Date", value=datetime.today())
        with col2:
            details = st.text_input("Details")
        with col3:
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        
        debit_or_credit = st.selectbox("Type", ["Debit", "Credit"])
        category = st.selectbox("Category", get_categories() or ["Uncategorized"])
        if st.button("Add Transaction"):
            insert_transactions(pd.DataFrame([{
                "date": pd.to_datetime(date),
                "details": details,
                "amount": amount,
                "debit_or_credit": debit_or_credit,
                "category": category
            }]))
            add_category(category)
            st.success("Transaction added.")
            st.rerun()

    debits = df[df["debit_or_credit"] == "Debit"].copy()
    credits = df[df["debit_or_credit"] == "Credit"].copy()

    tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
    
    #display tabs with credit vs debit transactions
    with tab1: 

        #make display better - editable dataframe
        with st.expander("Add Category"):
            new_category = st.text_input("New Category Name")
            if st.button("Add Category"):
                if new_category not in get_categories():
                    add_category(new_category)
                    reapply_keywords()
                    st.success(f"Category '{new_category}' added.")
                    st.rerun()

        st.subheader("Your Expenses")

        editable_df = debits[["id", "date", "details", "amount", "category"]].copy()
        
        available_categories = get_categories()
        if not available_categories:
            available_categories = ["Uncategorized"]

        edited_df = st.data_editor(
            editable_df,
            column_config={
                "id": st.column_config.TextColumn("ID", disabled=True),
                "date": st.column_config.DateColumn("Date", format="MM/DD/YYYY"),
                "details": st.column_config.TextColumn("Details"),
                "amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                "category": st.column_config.SelectboxColumn("Category", options=available_categories)
            }, 
            hide_index=True,
            use_container_width=True,
            key="category_editor"
        )

        save_button = st.button("Apply Changes", type="primary")
        #apply changes to database
        if save_button:
            #compared edited to originally and chooses category based on keyword
            changes_made = False
            for idx, row in edited_df.iterrows():
                transaction_id = row["id"]
                new_cat = row["category"]

                original_row = debits[debits["id"] == transaction_id]
                if not original_row.empty:
                    original_cat = original_row.iloc[0]["category"]

                    if new_cat != original_cat:
                        with get_connection() as conn:
                            conn.execute(
                                "UPDATE transactions SET category = ? WHERE id = ?",
                                (new_cat, transaction_id)
                            )
                            conn.commit()

                        add_keyword(new_cat, row["details"])
                        changes_made = True
            if changes_made:
                reapply_keywords()
                st.success("Changes applied.")
                st.rerun()
            else:
                st.info("No changes made")


        st.subheader('Expense Summary')

        total_expenses = debits["amount"].sum()
        st.metric("Total Expenses", f"{total_expenses:,.2f} AED")

        category_totals = debits.groupby("category")["amount"].sum().reset_index()
        category_totals = category_totals.sort_values("amount", ascending=False)

        st.dataframe(
            category_totals,
            column_config={
                "amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
            },
            use_container_width=True,
            hide_index=True
            )

        st.divider()

        #pie chart separated by category
        st.subheader("Expenses by Category")
        fig = px.pie(
            category_totals,
            values="amount",
            names="category",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Monthly Expense Trend")
        debits["month"] = debits["date"].dt.to_period("M").astype(str)
        monthly = debits.groupby("month")["amount"].sum().reset_index()
        fig = px.bar(monthly, x="month", y="amount")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Category Over Time Heatmap")
        heatmap_df = debits.groupby(["category", "month"])["amount"].sum().unstack(fill_value=0)
        fig = px.imshow(heatmap_df, labels=dict(x="month", y="category", color="amount"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2: 
        st.subheader("Payments Summary")
        total_payments = credits["amount"].sum()
        st.metric("Total Payments", f"{total_payments:,.2f} AED")
        
        st.dataframe(
            credits[["date", "details", "amount"]],
            column_config={
                "date": st.column_config.DateColumn("Date", format="MM/DD/YYYY"),
                "details": st.column_config.TextColumn("Details"),
                "amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
            },
            hide_index=True,
            use_container_width=True
        )


if __name__ == "__main__":
    main()