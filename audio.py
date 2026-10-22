import math
import wave
import io
import struct
import array



def notes_to_wav(notes, bpm=130):
    step_duration = 60 / bpm / 4
    all_samples = []
    dot = int(step_duration * 44100)
    for note in notes:
        if note is None:
            all_samples.extend([0]*dot)
        else:
            freq=midi_to_freq(note)
            note_samples=[]
            for i in range(dot):
                t = i / 44100
                envelope = 1.0 - (i / dot)
                value = 0.3 * envelope * math.sin(2 * math.pi * freq * t)
                sample = int(value * 32767)
                note_samples.append(sample)
            all_samples.extend(note_samples)
    return all_samples

def midi_to_freq(midi):
    freq = 440 * 2 ** ((midi-69) / 12)
    return freq

def save_to_wav(samples, filename, sample_rate=44100):
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        audio_array = array.array("h", samples)

        wav_file.writeframes(audio_array.tobytes())
    buffer.seek(0)

    with open(filename, "wb") as f:
        f.write(buffer.getvalue())
    return buffer

