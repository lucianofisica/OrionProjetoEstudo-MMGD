# This is a custom configuration file for Apache Superset.
# It allows us to override default settings.

# Enable template processing in SQL Lab, which allows for using Jinja templates
# in SQL queries for more dynamic analysis.
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

# Set the SQLAlchemy connection string for the Superset metadata database.
# This is configured to use the 'superset-db' service from docker-compose.
SQLALCHEMY_DATABASE_URI = "postgresql://superset:superset@superset-db:5432/superset"

# A function to run after the app is initialized
def app_init_hook(app):
    # Any custom app initialization logic can go here
    pass
