# Use the official Python image as a base
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy the setup script, requirements file, and Gunicorn configuration
COPY setup_dependencies.sh requirements.txt gunicorn.conf.py setup.py ./

# Make the setup script executable
RUN chmod +x setup_dependencies.sh

# Install the submodule dependencies
RUN ./setup_dependencies.sh

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 3100

# Healthcheck (optional, for production use)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
    CMD curl --fail http://localhost:3100/health || exit 1

# Run the application
CMD ["gunicorn", "api.main:app"]