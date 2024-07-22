FROM yannickbodin/ecn_ua_base_env:1.0 as build_image

# Install dependencie
COPY requirements.txt requirements.txt

# Create virtual environment
RUN python3 -m venv /venv

# Activate virtual environment
ENV PATH="/venv/bin:$PATH"

# Install dependencies
RUN pip install -r requirements.txt


# Start from a base image
FROM build_image as final_image 
# Copy the rest of your application
COPY . /app/

# Expose the port your app runs on
EXPOSE 1308

# Command to run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "1308"]
#CMD ["python3", "./OPC_client.py"]