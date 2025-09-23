# Stage 1 - Base image
FROM python:3.12-slim AS base

# Create app directory
WORKDIR /app

# Copy dependencies definition
COPY pyproject.toml uv.lock* ./

# Install uv (modern Python package manager)
RUN pip install uv

# Sync project dependencies
RUN uv sync --frozen

# Now copy actual source code
COPY . .

# Run as non-root user for security
RUN useradd -m appuser
USER appuser

# Default command = run your entrypoint (adjust based on your app)
CMD ["uv", "run", "python", "main.py"]