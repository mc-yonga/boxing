FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY boxing-analyst/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY boxing-analyst/ .

# Expose port (Railway will override this with $PORT)
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run streamlit
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.fileWatcherType none --browser.gatherUsageStats false
