from flask import Flask, request, jsonify
from nlp import generate_sql
from database import execute_query
from sql_query_parser import clean_sql_query

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.json.get('query')
    sql_query = generate_sql(user_input)
    cleaned_query = clean_sql_query(sql_query)
    results = execute_query(cleaned_query)
    return jsonify({'sql': cleaned_query, 'results': results})

if __name__ == '__main__':
    app.run(debug=True)