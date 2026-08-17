# =============================================================================
# Test Commands for Docker Stack
# =============================================================================

# Step 1: Build and start all services
docker compose up -d --build

# Step 2: Check logs (watch mode)
docker compose logs -f

# Step 3: Wait for health checks
sleep 45  # ~30s startup + 15s health confirmations

# Step 4: Verify all services healthy
docker compose ps

# Step 5: Call health endpoint
curl http://localhost:8000/health

# Step 6: Stop containers
docker compose down
