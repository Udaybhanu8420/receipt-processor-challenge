# Use the official Python slim image.
FROM python:3.10-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose port 8000 for the application.
EXPOSE 8000

# Run the FastAPI application with uvicorn.
CMD ["uvicorn", "processor:app", "--host", "0.0.0.0", "--port", "8000"]
