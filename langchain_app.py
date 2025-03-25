from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain import hub
from typing_extensions import Annotated, TypedDict
import vertexai

# Initialize Vertex AI
vertexai.init(project="", location="")
llm = init_chat_model("gemini-2.0-pro-exp-02-05", model_provider="google_vertexai")

# DB Setup
db_user = ""
db_password = ""
db_host = ""
db_name = ""
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)

# System Prompt
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(question):
    prompt_obj = query_prompt_template.invoke({
        "dialect": db.dialect,
        "top_k": 10,
        "table_info": db.get_table_info(),
        "input": question,
    })
    prompt_text = "\n".join([msg.content for msg in prompt_obj.messages])
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt_text)
    return result["query"]

def execute_query(query):
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return execute_query_tool.invoke(query)

def generate_answer(question, query, result):
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {question}\n'
        f'SQL Query: {query}\n'
        f'SQL Result: {result}'
    )
    response = llm.invoke(prompt)
    return response.content

def process_question(question):
    query = write_query(question)
    result = execute_query(query)
    answer = generate_answer(question, query, result)
    return query, result, answer
