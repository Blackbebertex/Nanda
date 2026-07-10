# ARTHA AI Avatar Voice Synthesizer

def synthesize(text):
    # Legacy compatibility fallback returning raw bytes
    return b"audio_data"

def synthesize_voice_details(text, language="en"):
    """
    Computes speech duration and lipsync viseme cues for the frontend avatar.
    Returns: audio URL, duration (ms), and an array of timestamped viseme shapes.
    """
    words = str(text).split()
    word_count = len(words)
    
    # Estimate speech duration: ~300ms per word + 500ms padding
    duration_ms = max(1200, (word_count * 300) + 500)
    
    viseme_shapes = ["closed", "open_wide", "narrow", "open_mild", "wide_smile", "closed"]
    cues = [{"atMs": 0, "shape": "closed"}]
    
    # Compute step intervals dynamically (e.g. one viseme every 250ms)
    interval = 250
    current_time = 0
    idx = 1
    
    while current_time < duration_ms - 300:
        current_time += interval
        shape = viseme_shapes[idx % len(viseme_shapes)]
        cues.append({"atMs": current_time, "shape": shape})
        idx += 1
        
    cues.append({"atMs": duration_ms, "shape": "closed"})
    
    # Provide a stable public demo audio file URL
    audio_url = "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
    
    return {
        "audio_url": audio_url,
        "duration_ms": duration_ms,
        "viseme_cues": cues
    }