# Use the official Apache Spark image as the base
FROM apache/spark:3.4.1

# Switch to the root user to install dependencies
USER root

# Set the working directory in the container
WORKDIR /app

# Install SageMaker inference toolkit and any additional dependencies
RUN apt-get update && apt-get install -y python3-pip && \
    pip install --no-cache-dir sagemaker-inference

# Copy the application code to the working directory
COPY app /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the pre-trained model
COPY app/als_model /app/als_model

# Expose the application port
EXPOSE 8080

# Set environment variables required by SageMaker
ENV SAGEMAKER_PROGRAM serve.py

# Define the entry point for the container
ENTRYPOINT ["python3", "/app/serve.py"]

# Set the default command to run the SageMaker-compatible server
CMD ["serve"]
