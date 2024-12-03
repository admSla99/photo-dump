FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Use environment variable for port
ENV PORT=8501

# Expose port
EXPOSE $PORT

# Create startup script
RUN echo '#!/bin/bash\n\
python app.py & \
streamlit run --server.port $PORT --server.address 0.0.0.0 streamlit_app.py\
' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
