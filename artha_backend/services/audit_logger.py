import json
import datetime
import os
import hashlib

def log_event(event_data):
    """
    Appends events to a secure local audit trail.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    log_record = {
        "timestamp": timestamp,
        "payload": event_data
    }
    
    # Generate verification signature hash for audit integrity
    serialized = json.dumps(log_record, sort_keys=True)
    record_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    log_record["integrity_hash"] = record_hash
    
    # Print to system console
    print(f"[AUDIT] {serialized}")
    
    # Append to local file
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file = os.path.join(base_dir, "audit.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_record) + "\n")
    except Exception as e:
        print(f"Failed to write to audit log file: {e}")
        
    return log_record