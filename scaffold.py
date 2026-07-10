import os

backend_dir = r'd:\IDBI\artha_backend'
os.makedirs(os.path.join(backend_dir, 'services'), exist_ok=True)
os.makedirs(os.path.join(backend_dir, 'agents'), exist_ok=True)

gateway_code = '''
from fastapi import FastAPI
app = FastAPI(title="ARTHA API Gateway")
@app.post("/v1/session/start")
def start_session():
    return {"status": "Session Initialized", "session_id": "12345"}
@app.post("/v1/consent/request")
def request_consent():
    return {"status": "Consent Requested"}
'''
with open(os.path.join(backend_dir, 'main.py'), 'w', encoding='utf-8') as f:
    f.write(gateway_code)

services = {
    'consent_service.py': 'def check_consent(user_id): return True',
    'customer_snapshot.py': 'def get_snapshot(user_id): return {"savings": 50000, "debts": 1000}',
    'behaviour_engine.py': 'def compute_signals(transactions): return {"savings_rate": 0.22}',
    'advisory_engine.py': 'def get_recommendation(snapshot): return {"action": "increase_emergency_fund"}',
    'rm_handoff.py': 'def trigger_handoff(user_id, reason): return {"status": "escalated"}',
    'audit_logger.py': 'def log_event(event_data): print("AUDIT:", event_data)'
}
for name, content in services.items():
    with open(os.path.join(backend_dir, 'services', name), 'w', encoding='utf-8') as f:
        f.write(content)

agents = {
    'rag_knowledge_base.py': 'def retrieve_facts(query): return ["Fact 1: FD interest is 6.1%"]',
    'ai_orchestrator.py': 'def generate_response(intent): return "Here is your wealth guidance."',
    'compliance_guardrails.py': 'def check_safety(response): return True',
    'avatar_voice.py': 'def synthesize(text): return b"audio_data"'
}
for name, content in agents.items():
    with open(os.path.join(backend_dir, 'agents', name), 'w', encoding='utf-8') as f:
        f.write(content)

frontend_dir = r'd:\IDBI\artha_frontend'
os.makedirs(frontend_dir, exist_ok=True)
index_html = '''
<!DOCTYPE html>
<html>
<head><title>ARTHA Mobile Module</title></head>
<body>
    <div id="app">
        <h1>ARTHA Copilot</h1>
        <div id="chat"></div>
        <input type="text" id="user_input" placeholder="Ask Artha..." />
        <button>Send</button>
    </div>
</body>
</html>
'''
with open(os.path.join(frontend_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

print('Phase 2 MVP Backend and Frontend skeletons created.')
