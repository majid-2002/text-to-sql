from google import genai
from get_schema_metadata import get_schema_metadata

# GEMINI API Key
client = genai.Client(api_key="")

SCHEMA_METADATA = None

def handle_incompleteness(user_input):
    if len(user_input.split()) < 3:
        return f"Your query seems incomplete. Please provide more details."
    return None


def generate_sql(user_input):
    global SCHEMA_METADATA 

    if SCHEMA_METADATA is None:
        SCHEMA_METADATA = get_schema_metadata()

    incompleteness_response = handle_incompleteness(user_input)
    if incompleteness_response:
        return incompleteness_response

    prompt = f"""
    Generate an SQL query based on the user's input for the Pagila database.

    ### Schema Rules:
    - Use only these tables: {', '.join(SCHEMA_METADATA["tables"])}
    - Ensure correct column names: {SCHEMA_METADATA["columns"]}
    - 'release_year' is an INTEGER (do not use EXTRACT())
    - 'rental_date' is a TIMESTAMP (use proper date functions)
    - 'actor_name' should be UPPERCASE
    - Join tables correctly based on foreign key relationships: {SCHEMA_METADATA["relationships"]}

    User Query: "{user_input}"
    If the input is ambiguous, provide clarification. Return ONLY the SQL query.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    try:
        sql_query = response.text.strip()
        if not sql_query:
            return "Error: The AI did not return a valid SQL query."
        return sql_query
    except AttributeError:
        return "Error: Failed to parse AI response."