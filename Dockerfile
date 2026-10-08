FROM python:3.11-slim
WORKDIR /app
# COPY persistent_auditor.py .
CMD ["python", "inventory.py"]