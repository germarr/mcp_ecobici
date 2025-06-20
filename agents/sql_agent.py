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
CREATE TABLE records (
genero_usuario  VARCHAR,
edad_usuario   BIGINT,
 bici  VARCHAR,
ciclo_estacion_retiro  VARCHAR,
fecha_retiro  VARCHAR,
ciclo_estacionarribo  VARCHAR,
fecha_arribo  VARCHAR,
fecha_retiro_completa  VARCHAR,
fecha_arribo_completa  VARCHAR,
time_between_trips   DOUBLE,
day_of_the_week  VARCHAR,
is_weekend   BIGINT,
lat_start   DOUBLE,
lon_start   DOUBLE,
lat_end   DOUBLE,
lon_end   DOUBLE,
distance_meters   DOUBLE,
hora_retiro  VARCHAR,
hora_arribo  VARCHAR
);
"""

SQL_EXAMPLES = [
    {
        'request': 'show me the total trips by gender',
        'response': "SELECT genero_usuario, COUNT(*) as trips FROM bike_trips GROUP BY genero_usuario",
    },
    {
        'request': 'show me the total number of trips by day of the week',
        'response': "SELECT day_of_the_week, COUNT(*) as trips FROM bike_trips GROUP BY day_of_the_week ",
    },
    {
        'request': 'show me records from yesterday',
        'response': "SELECT * FROM bike_trips WHERE fecha_arribo::date > CURRENT_TIMESTAMP - INTERVAL '1 day'",
    },
    {
        'request': 'show me the total time spent between trips and the total distance traveled',
        'response': """
            SELECT fecha_arribo,day_of_the_week, ROUND(SUM(time_between_trips),2) as time_between_trips, 
        ROUND(SUM(distance_meters),2) as distance_meters 
        FROM bike_trips 
        GROUP BY fecha_arribo,day_of_the_week
        """,
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
Given the following SQLITE table of records, your job is to
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
