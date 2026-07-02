import os

ops_dir = r'd:\IDBI\phase_4_5_ops'
os.makedirs(ops_dir, exist_ok=True)

deliverables = {
    'Dockerfile': '''FROM python:3.10-slim
WORKDIR /app
COPY ./artha_backend /app
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''',
    'docker-compose.yml': '''version: '3.8'
services:
  artha_gateway:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - LOG_LEVEL=info
  artha_frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ../artha_frontend:/usr/share/nginx/html
''',
    '.github/workflows/ci_cd.yml': '''name: ARTHA CI/CD
on:
  push:
    branches: [ main ]
jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Run Tests
      run: python -m unittest discover -s artha_backend/tests
    - name: Build Docker Image
      run: docker build -t artha-gateway .
''',
    'operations_runbook.md': '''# ARTHA Operations Runbook (Phase 4/5)
**Incident Handling:**
- SEV-1 (Critical): Stop autonomous workflows, trigger manual RM override.
- SEV-2 (Degraded): Use fallback static messaging.

**Deployment Checklist:**
1. Monitor AI safety metrics for first 48 hours post-deployment.
2. Verify Account Aggregator live keys.
3. Validate PII masking in production logs.
''',
    'sla_dashboard_config.json': '''{
  "dashboard": "ARTHA AI Pilot & Production",
  "metrics": [
    {"name": "API Latency", "threshold_ms": 500, "action": "alert_engineering"},
    {"name": "Hallucination Incidents", "threshold_count": 0, "action": "block_service_alert_compliance"},
    {"name": "Consent Failures", "threshold_percent": 2, "action": "alert_product_team"}
  ]
}
'''
}

for name, content in deliverables.items():
    filepath = os.path.join(ops_dir, name)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Phase 4 and 5 Operations files created.')
