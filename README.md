---

# **Text-to-SQL Agent for Pagila Database**  

## **📌 Overview**  
This project is a **Flask-based Text-to-SQL Agent** that converts natural language queries into **SQL queries** for the Pagila database.  
It leverages **Google's Gemini AI** for query generation and connects to a **PostgreSQL database** to execute the queries.  

---

## **📂 Project Structure**  

```
📦 text-to-sql-agent
├── app.py                 # Flask API for handling user queries
├── nlp.py                 # Query processing and LLM integration
├── get_schema_metadata.py  # Extracts schema details from the Pagila database
├── requirements.txt       # Required dependencies
├── README.md              # Project documentation
```

---

## **⚙️ Setup Instructions**  

### **1️⃣ Install Dependencies**  
Ensure you have **Python 3.8+** installed. Then, install required packages:  

```sh
pip install -r requirements.txt
```

---

### **2️⃣ Set Up the Database**  
Setup the Pagilla database by using docker-compose.  

```python
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)


```
### **3️⃣ Set Up the API**

Replace the `REPLACE_YOUR_APIKEY` with your Gemini API key in `nlp.py` file.
```
client = genai.Client(api_key="REPLACE_YOUR_APIKEY")

```


---

### **3️⃣ Run the Flask Server**
Start the Flask server:  

```sh
python app.py
```

It will run on `http://127.0.0.1:5000/` by default.

---

### **4️⃣ Send API Requests**  

Use **cURL** or **Postman** to send requests.  

#### **➡️ Sample Request (POST `/query`)**  
```json
{
    "query": "List all actors' first and last names."
}
```

#### **⬅️ Sample Response**  
```json
{
    "sql": "SELECT first_name, last_name FROM actor;",
    "results": [
        ["John", "Doe"],
        ["Jane", "Smith"]
    ]
}
```

---
## **🚀 Future Enhancements**
- Add **vector search** for better query understanding  
- Implement **fine-tuned LLM models** for more accurate SQL generation  
---
