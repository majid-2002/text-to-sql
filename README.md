
# **Text-to-SQL Agent for Pagila Database**  

## **📌 Overview**  
This project is a **Flask-based Text-to-SQL Agent** that converts natural language queries into **SQL queries** for the Pagila database.  
It leverages **Google's Gemini AI** for query generation and connects to a **PostgreSQL database** to execute the queries.  

---

## **⚙️ Setup Instructions**  

### **1️⃣ Clone the Repository**  
First, clone the project repository from GitHub:  

```sh
git clone https://github.com/majid-2002/text-to-sql.git
cd text-to-sql
```

---

### **2️⃣ Set Up a Virtual Environment**  
It's recommended to use a **virtual environment** to manage dependencies.  

#### **For Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

#### **For macOS/Linux:**
```sh
python3 -m venv venv
source venv/bin/activate
```

---

### **3️⃣ Install Dependencies**  
After activating the virtual environment, install the required dependencies:  

```sh
pip install -r requirements.txt
```

---

### **4️⃣ Set Up the Database**  
Set up the **Pagila database** using **Docker Compose** and update the database connection details in `database.py`:  

```python
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",  # username
    password="123456",  # password
    host="localhost",
    port="5432"
)
```


---

### **5️⃣ Set Up the API Key**  
Replace the placeholder `REPLACE_YOUR_APIKEY` with your **Google Gemini API Key** in `nlp.py`:  

```python
client = genai.Client(api_key="REPLACE_YOUR_APIKEY")
```

---

### **6️⃣ Run the Flask Server**  
Start the Flask server **inside the virtual environment**:  

```sh
python app.py
```

The API will be available at **`http://127.0.0.1:5000/`**.

---

### **7️⃣ Send API Requests**  

You can use **cURL** or **Postman** to test the API.

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
