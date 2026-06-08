# Personal Finance Tracker

Personal Finance Tracker is a Streamlit app for uploading, organizing, and analyzing personal bank transactions. It uses pandas and SQLite to store transaction data and Plotly to display spending visualizations.

## Features

- Upload a CSV bank statement
- Save transactions to a SQLite database
- Add transactions manually
- View expenses and payments separately
- Categorize expenses
- Add custom categories
- Save keywords for automatic categorization
- View total expenses and payments
- View spending by category
- View monthly expense trends
- View category spending over time

## Tech Stack

- Python
- Streamlit
- pandas
- Plotly
- SQLite

## Project Structure

```text
personal-finance-tracker/
├── database.py
├── finance_data.db
├── main.py
└── sample_bank_statement.csv
```

## CSV Format

The uploaded CSV file should include the following columns:

```text
Date
Details
Amount
Debit/Credit
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jennarentz/projects.git
cd projects/personal-finance-tracker
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install streamlit pandas plotly
```

## How to Run

From the `personal-finance-tracker` folder:

```bash
streamlit run main.py
```

The app will open in your browser.

## How to Use

1. Open the Streamlit app.
2. Upload a CSV bank statement.
3. Review your transactions.
4. Add new transactions manually if needed.
5. Create custom categories.
6. Categorize expenses in the editable table.
7. Apply changes to save category updates.
8. View spending summaries and charts.

## Notes

The dashboard currently uses AED as the currency format. To use another currency, update the currency formatting in `main.py`.

## Future Improvements

- Add a `requirements.txt` file
- Add support for multiple currencies
- Add date range filters
- Add income vs. expense comparison charts
- Add export options for categorized transactions
- Move the SQLite database file out of version control
