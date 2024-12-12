# Use an official base image, such as Python for a Python app
FROM python:3.11-slim

WORKDIR /Users/andre/PycharmProjects/ProgramareaInRetea


COPY . .

# Install any necessary dependencies from requirements.txt
RUN pip install -r requirements.txt


# Expose the port your app runs on, for example, 5000 for Flask
EXPOSE 5000
EXPOSE 8765

# Define the command to run the app
CMD ["python", "app.py"]
