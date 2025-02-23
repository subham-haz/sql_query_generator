import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000/chat"  # Change if running on a different port

st.title("🔍 AI-Powered SQL Chatbot")
st.write("Enter your natural language query, and the AI will generate and execute the SQL query.")

# User input
user_query = st.text_area("Enter your query:", placeholder="Show total sales by category for the last month.")

if st.button("Generate SQL & Execute"):
    if user_query.strip():
        with st.spinner("Generating SQL and fetching results..."):
            # Send request to FastAPI backend
            response = requests.post(BACKEND_URL, json={"user_input": user_query})

            if response.status_code == 200:
                data = response.json()
                sql_query = data.get("sql", "No SQL generated")
                results = data.get("results", [])
                columns = data.get("columns", [])  # Expecting column names from API

                st.subheader("📝 Generated SQL Query")
                st.code(sql_query, language="sql")

                st.subheader("📊 Query Results")
                if isinstance(results, list) and results:
                    # Convert results into DataFrame with correct column names
                    if columns and len(columns) == len(results[0]):  
                        df = pd.DataFrame(results, columns=columns)
                    else:  
                        df = pd.DataFrame(results, columns=[f"Column {i+1}" for i in range(len(results[0]))])

                    st.dataframe(df.style.set_properties(**{
                        'background-color': 'white',
                        'color': 'black',
                        'border-color': 'black'
                    }))
                else:
                    st.warning("⚠️ No results found. The query might be incorrect or return no data.")
            else:
                st.error("❌ Error connecting to backend. Check FastAPI server.")
    else:
        st.warning("⚠️ Please enter a query.")
