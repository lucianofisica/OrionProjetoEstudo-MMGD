# This Dockerfile creates an image for running the dbt project.
# Airflow will use this image with the DockerOperator to run dbt tasks.

FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /dbt

# Copy the requirements file and install Python dependencies
# We copy only the requirements first to leverage Docker layer caching.
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire dbt project into the container
COPY . .

# Copy the profiles.yml into the default dbt directory in the container.
# This makes the image self-contained and ready to run.
COPY ./profiles.yml /root/.dbt/profiles.yml

# Define the entrypoint for the container.
# This allows us to run dbt commands directly.
ENTRYPOINT ["dbt"]
