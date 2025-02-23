import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import psycopg2
from fuzzywuzzy import process

# Load environment variables
load_dotenv()

# PostgreSQL connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "business_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")

# Get Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY is not set in environment variables.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_table_names():
    """Fetches all table names from the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public';")

        tables = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"⚠️ Error fetching table names: {e}")
        return []


def find_best_table_match(user_input, table_names):
    """Finds the best matching table name from the database schema."""
    best_match, score = process.extractOne(user_input, table_names) if table_names else (None, 0)

    return best_match if score > 70 else None


def generate_sql_query(user_input):
    """Generate an optimized PostgreSQL SQL query from user input using Gemini AI."""
    
        # Detect if the user wants to see available tables
    keywords = ["show tables", "list tables", "available tables", "database tables"]
    if any(keyword in user_input.lower() for keyword in keywords):
        return "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public';"

    
    # Get latest table names from the database
    table_names = get_table_names()

    # Try to find the correct table name
    best_table = find_best_table_match(user_input, table_names)

    if not best_table:
        return "Error: Unable to determine the correct table name. Please check your input."

    prompt = f"""
    You are an AI SQL assistant that translates natural language into **correct, optimized, and efficient** PostgreSQL queries.  
    Your task is to understand the user request and generate a **valid SQL query** that retrieves the required data **accurately and efficiently**.  
    **Follow these rules strictly:**
    
    ### **1️⃣ General Rules**
    - **Always use PostgreSQL syntax** (e.g., `NOW()`, `INTERVAL '1 month'`, `ILIKE` for case-insensitive searches).  
    - **Do NOT use markdown formatting** (````sql` or ` ``` `). Just return the raw SQL query.  
    - **Alias columns when aggregating** (e.g., `SUM(sales) AS total_sales`).  
    - **Use explicit column names** instead of `SELECT *` for clarity and performance.  

    ### **2️⃣ Handling Database Schema**
    - The table name for this query is: `{best_table}`.  
    - If **column names are unknown**, make an educated guess based on the query context.  

    ### **3️⃣ Query Optimization**
    - Use **indexes when applicable** (e.g., indexed columns in `WHERE` clauses).  
    - Optimize **filtering conditions** (e.g., avoid `LIKE '%keyword%'` unless necessary).  
    - **Use JOINS instead of subqueries** whenever possible for performance.  

    ### **4️⃣ Handling Different Query Types**
    Your generated SQL should correctly handle:  
    - **Basic Queries** (e.g., "Show all employees in the sales department.")  
    - **Aggregations** (e.g., "Get total revenue by region.")  
    - **Filtering Conditions** (e.g., "List customers who joined in the last 6 months.")  
    - **Sorting and Grouping** (e.g., "Rank employees by sales performance.")  
    - **Joins Across Multiple Tables** (e.g., "Get order details with customer names.")  
    - **Date and Time Queries** (e.g., "Show transactions from the last 30 days.")  
    - **Conditional Queries** (e.g., "Find products where stock is low but demand is high.")  
    - **User-defined Constraints** (e.g., "Fetch all orders above $500 placed in New York.")  

    **Example Queries and Outputs:**

    **User:** Show total sales by category for the last month.  
    **SQL:**  
    SELECT category, SUM(sales) AS total_sales  
    FROM {best_table}  
    WHERE date >= NOW() - INTERVAL '1 month'  
    GROUP BY category;

    **User Query:**  
    "{user_input}"  

    **SQL Query (PostgreSQL compatible):**
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text.strip()


def execute_sql_query(sql_query):
    """Executes the SQL query and returns the results along with column names."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        cur.execute(sql_query)  # Execute query
        results = cur.fetchall()  # Fetch all rows
        column_names = [desc[0] for desc in cur.description]  # Extract column names

        cur.close()
        conn.close()

        return {"columns": column_names, "results": results}  # Return results with column names

    except Exception as e:
        return {"error": str(e)}



def clean_sql_query(sql_query):
    """Removes Markdown formatting and converts MySQL syntax to PostgreSQL."""
    # Remove Markdown code block markers (```sql ... ```)
    sql_query = re.sub(r"```sql\n|\n```", "", sql_query, flags=re.IGNORECASE)

    # Convert MySQL DATE_SUB to PostgreSQL INTERVAL syntax
    sql_query = re.sub(r"DATE_SUB\(NOW\(\), INTERVAL (\d+) (DAY|MONTH|YEAR)\)", r"NOW() - INTERVAL '\1 \2'", sql_query, flags=re.IGNORECASE)

    return sql_query.strip()


def process_query(natural_language_query):
    """Converts user query to SQL, executes it, and returns results with column names."""
    generated_sql = generate_sql_query(natural_language_query)  # Generate SQL

    if "Error" in generated_sql:
        return {"error": generated_sql}  # Return error if table detection fails

    clean_sql = clean_sql_query(generated_sql)  # Remove Markdown formatting
    
    print('Clean SQL:', clean_sql)

    # Execute the cleaned SQL query
    query_response = execute_sql_query(clean_sql)

    if "error" in query_response:
        return query_response  # Return error if execution fails

    return {
        "sql": clean_sql,
        "columns": query_response["columns"],  # Include column names
        "results": query_response["results"]
    }

