# Use a base image with Python (adjust the version as needed)
FROM python:3.11-slim-buster

# Set the working directory
WORKDIR /src

# Copy the .env to retrieve the API key
COPY .env /src/

# Copy the poetry files to the working directory
COPY pyproject.toml poetry.lock /src/

# Install poetry
RUN pip install poetry==1.2.0

# Install the project dependencies
RUN poetry config virtualenvs.create false && poetry install 

# Copy the application code
COPY app/utils.py /src/
COPY app/app.py /src/
COPY app/get_fare_rules_from_API.py /src/
COPY app/get_fare_rules_from_DB.py /src/
COPY app/scrapping.py /src/
COPY app/prompt_fill_template.py /src/
COPY app/website_list.xlsx /src/
COPY app/db_flights_par_mad_doh.csv /src/
COPY app/fare_data_json/ /src/fare_data_json/

# Expose the port your application is running on (adjust if needed)
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Command to run your Streamlit app
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
