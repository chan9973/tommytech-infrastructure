# =============================================================================
# Multi-stage Build: Minimal Runtime Image (non-root FastAPI)
# Stage 1: Builder - Install dependencies
# Stage 2: Runtime - Copy only runtime files in non-root user
# =============================================================================

# Stage 1: Builder (install dependencies)
FROM python:3.12-slim as builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Stage 2: Runtime (non-root, minimal)
FROM python:3.12-slim as runtime

# Add user and group for non-root execution
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Copy wheels from builder stage
COPY --chown=appuser:appgroup --from=builder /wheels /wheels

WORKDIR /app

# Install runtime dependencies only
RUN pip install --no-cache-dir --no-deps -r requirements.txt \
&& rm -rf /root/.cache

# Copy application code (non-root ownership)
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Health check (exposed in docker-compose healthcheck section)
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
