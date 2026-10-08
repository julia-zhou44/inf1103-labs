FROM python:3.11-slim
WORKDIR /app
# COPY persistent_auditor.py .
COPY inventory.py .
CMD ["python", "inventory.py"]