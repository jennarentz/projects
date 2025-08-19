import sqlite3
import pandas as pd

DB_FILE = "finance_data.db"

#connects file from user to database
def get_connection():
    return sqlite3.connect(DB_FILE)

#creates tables for transactions, categories, and keywords for auto-categorization
#execute sends statement with command to database
#needs id to access rows later
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                details TEXT,
                amount REAL,
                debit_or_credit TEXT,
                category TEXT DEFAULT 'Uncategorized'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT PRIMARY KEY
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                category TEXT,
                keyword TEXT,
                PRIMARY KEY (category, keyword),
                FOREIGN KEY (category) REFERENCES categories(name)
            )
        ''')
        conn.commit()

#adds a new category to database if doesn't exist
def add_category(name):
    with get_connection() as conn: 
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
        conn.commit()

#returns a list of category names
def get_categories():
    with get_connection() as conn:
        return [row[0] for row in conn.execute("SELECT name FROM categories").fetchall()]
    
#returns a dictionary mapping each category to a list of keywords
def get_keywords():
    with get_connection() as conn:
        cursor = conn.execute("SELECT category, keyword FROM keywords")
        keywords = {}
        for category, keyword in cursor:
            keywords.setdefault(category, []).append(keyword.strip().lower())
        return keywords
    
def add_keyword(category, keyword):
    add_category(category)
    keyword = keyword.strip().lower()

    with get_connection() as conn:
        conn.execute('''
            INSERT OR IGNORE INTO keywords (category, keyword)
            VALUES (?, ?)
        ''', (category, keyword))

        #updates transactions with matching details
        conn.execute('''
            UPDATE transactions
            SET category = ?
            WHERE LOWER(TRIM(details)) = ?
        ''', (category, keyword))

        # Also update transactions that match any keyword in the list 
        # Get all keywords for this category
        cursor = conn.execute('SELECT keyword FROM keywords WHERE category = ?', (category,))
        keyword_list = [row[0].strip().lower() for row in cursor]
        
        # For each keyword, update transactions whose details *contain* that keyword
        for kw in keyword_list:
            conn.execute('''
                UPDATE transactions
                SET category = ?
                WHERE LOWER(details) LIKE ?
            ''', (category, f"%{kw}%"))
        
        conn.commit()

def reapply_keywords():
    keywords = get_keywords()
    with get_connection() as conn:
        for category, keyword_list in keywords.items():
            for keyword in keyword_list:
                conn.execute('''
                    UPDATE transactions
                    SET category = ?
                    WHERE LOWER(details) LIKE ?
                ''', (category, f"%{keyword}%"))
        conn.commit()

#takes a pandas dataframe and saves each row to transactions table
def insert_transactions(df):
    df["date"] = df["date"].dt.date
    with get_connection() as conn:
        for _, row in df.iterrows():
            #prevents duplicates - file being added continuously
            exists = conn.execute('''
                SELECT 1 FROM transactions
                WHERE date = ? AND amount = ? AND debit_or_credit = ? AND details = ?
            ''', (row["date"], row["amount"], row["debit_or_credit"], row["details"])
            ).fetchone()
            
            if not exists:
                conn.execute('''
                    INSERT INTO transactions (date, amount, debit_or_credit, details, category)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row["date"], row["amount"], row["debit_or_credit"], row["details"], row["category"]))
        conn.commit()

#loads saved transactions into a dataframe for display
def load_transactions():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM transactions", conn, parse_dates=["date"])