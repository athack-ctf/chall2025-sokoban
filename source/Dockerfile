# Use the official Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /chall

RUN pip install numpy

COPY main.py ./
COPY flag.txt ./
COPY solvable.json ./

# Set environment vars
ENV PORT=2025
ENV TIMEOUT=10000

# Expose the port that the chall will run on
EXPOSE 2025

# Run the chall
CMD ["python3", "main.py"]
