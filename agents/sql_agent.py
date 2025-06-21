from dotenv import load_dotenv
import os
from datetime import date
from typing import Annotated, Union
from annotated_types import MinLen
from pydantic import BaseModel, Field
from typing_extensions import TypeAlias

from pydantic_ai import Agent, format_as_xml

# Load environment variables from .env in the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Now you can access your key as:
openai_key = os.getenv("openaikey")
os.environ["OPENAI_API_KEY"] = openai_key
# Import BikeTrip from app.models


DB_SCHEMA = """
CREATE TABLE duckone_bikes (
fecha_arribo  VARCHAR,
first_day_of_month  VARCHAR,
day_of_the_week  VARCHAR,
distance_meters   INTEGER,
time_between_trips   DOUBLE,
total_trips  INTEGER
);
"""

SQL_EXAMPLES = [
    {
        'request': 'show me the total trips for October 21 of the year 2024',
        'response': "SELECT fecha_arribo, total_trips FROM duckone_bikes WHERE EXTRACT(year FROM fecha_arribo) = 2024 AND EXTRACT(month FROM fecha_arribo) = 10 AND EXTRACT(day FROM fecha_arribo) = 21",
    },
    {
        'request': 'show me the average distance traveled by day of the week',
        'response': "SELECT day_of_the_week, AVG(distance_meters) as avg_distance FROM duckone_bikes GROUP BY day_of_the_week",
    },
    {
        'request': 'show me the total time spent between trips for each month',
        'response': "SELECT first_day_of_month, SUM(time_between_trips) as total_time FROM duckone_bikes GROUP BY first_day_of_month",
    },
    {
        'request': 'show me the maximum distance traveled in a single trip',
        'response': "SELECT MAX(distance_meters) as max_distance FROM duckone_bikes",
    },
]


class Success(BaseModel):
    """Response when SQL could be successfully generated."""
    sql_query: Annotated[str, MinLen(1)]
    explanation: str = Field(
        '', description='Explanation of the SQL query, as markdown'
    )

class InvalidRequest(BaseModel):
    """Response when the user input didn't include enough information to generate SQL."""
    error_message: str

Response: TypeAlias = Union[Success, InvalidRequest]

agent = Agent[Response](
    'openai:gpt-4o',
    output_type=Response
)

@agent.system_prompt
def system_prompt() -> str:
    return f"""
Given the following SQL table of records, your job is to
write a SQL query that suits the user's request. 
THE TABLE NAME IN ALL THE QUEIRES IS bike_trips

Database schema:

{DB_SCHEMA}

today's date = {date.today()}

{format_as_xml(SQL_EXAMPLES)}
"""

# Usage example:
if __name__ == '__main__':
    prompt = "show me the total trips by gender"
    result = agent.run_sync(prompt)
    print(result.output.sql_query)
