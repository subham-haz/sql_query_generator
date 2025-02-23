# AI-Powered SQL Chatbot

## 🚀 Overview

AI-Powered SQL Chatbot is a natural language interface that allows users to interact with a PostgreSQL database using plain English. The chatbot translates user queries into optimized SQL statements, executes them, and returns results in an easy-to-read format.

## 🏗 Tech Stack

- **Backend:** FastAPI (Python) with Gemini AI for SQL generation
- **Database:** PostgreSQL
- **Frontend:** Streamlit (for a simple UI)
- **Deployment:** Docker (optional), GitHub, Streamlit Cloud, or AWS/GCP

## 📌 Features

- Convert natural language queries into **valid, optimized SQL** statements
- Execute SQL queries **securely** on a PostgreSQL database
- Display results in a structured, user-friendly table
- Supports **aggregation, filtering, joins, and date-based queries**
- Provides **real-time error handling** for invalid SQL queries

## 📂 Project Structure

```
ai-sql-chatbot/
│── backend/              # FastAPI backend for query processing
│   ├── main.py           # FastAPI application entry point
│   ├── sql_generator.py  # AI-powered SQL generation logic
│   ├── db_connection.py  # PostgreSQL connection setup
│── frontend/             # Streamlit UI
│   ├── app.py            # Streamlit application
│── .env                  # Environment variables
│── Dockerfile            # Docker configuration (optional)
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```

## ⚙️ Installation & Setup

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/your-username/ai-sql-chatbot.git
cd ai-sql-chatbot
```

### 2️⃣ **Set Up the Environment**

Create a `.env` file and configure the following:

```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
GEMINI_API_KEY=your_gemini_api_key
```

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Run the Backend (FastAPI)**

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Test it by opening: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5️⃣ **Run the Frontend (Streamlit)**

```bash
streamlit run frontend/app.py
```

## 🧪 Testing

- Use **Postman** or a browser to test API endpoints at `http://localhost:8000/chat`
- Try different SQL queries via the **Streamlit UI**
- Check logs for debugging: `tail -f logs.txt`

## 🚀 Deployment

### **Option 1: Deploy on Streamlit Cloud** (Easiest)

1. Push your project to GitHub
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy your repo by linking it with your GitHub account

### **Option 2: Deploy on Docker**

1. Build the image:

```bash
docker build -t ai-sql-chatbot .
```

2. Run the container:

```bash
docker run -p 8000:8000 ai-sql-chatbot
```

### **Option 3: Deploy on AWS/GCP**

- Use **AWS EC2** or **Google Cloud Run** for scalable deployment
- Set up **PostgreSQL on RDS** (AWS) or **Cloud SQL** (GCP)

## ✨ Contributing

Feel free to submit **issues, feature requests, or pull requests**. Contributions are welcome!

## 📜 License

MIT License. See `LICENSE` for details.

---
