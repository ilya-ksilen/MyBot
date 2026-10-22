import numpy as np
import scipy.io.wavfile as wavf
import io

def notes_to_wav(notes, bpm=130, sample_rate=22050):
    total_steps = len(notes)
    step_duration_sec = 60.0 / bpm / 4.0
    
    total_samples = int(sample_rate * step_duration_sec * total_steps)
    
    audio_buffer = np.zeros(total_samples, dtype=np.float32)
    
    for step, note in enumerate(notes):
        if note is None:
            continue
            
        freq = 440.0 * (2.0 ** ((note - 69) / 12.0))
        
        start_sample = int(step * step_duration_sec * sample_rate)
        end_sample = min(int((step + 1) * step_duration_sec * sample_rate), total_samples)
        
        if end_sample <= start_sample:
            continue
            
        samples_count = end_sample - start_sample
        t = np.arange(samples_count) / sample_rate
        
        envelope = np.exp(-4.0 * t / step_duration_sec)
        
        signal = np.sin(2 * np.pi * freq * t)
        
        audio_buffer[start_sample:end_sample] += signal * envelope * 0.5
    
    max_val = np.max(np.abs(audio_buffer))
    if max_val > 0:
        audio_normalized = audio_buffer / max_val
    else:
        audio_normalized = audio_buffer
    
    audio_int16 = (audio_normalized * 32767).astype(np.int16)
    
    wav_io = io.BytesIO()
    wavf.write(wav_io, sample_rate, audio_int16)
    return wav_io.getvalue()