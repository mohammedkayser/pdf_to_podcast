import os
import time
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

class AudioGenerator:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.client.timeout = 300  # 5 minutes
    
    def get_voice(self):
        voices = self.client.voices.get_all().voices
        preferred = ['Rachel', 'Adam', 'Lily', 'Josh']
        for v in voices:
            if v.name in preferred:
                return v.voice_id
        return voices[0].voice_id if voices else None
    
    def chunk_text(self, text, max_chars=2500):
        sentences = text.split('. ')
        chunks, chunk = [], ""
        for sentence in sentences:
            if len(chunk) + len(sentence) + 2 > max_chars:
                chunks.append(chunk.strip() + '.')
                chunk = sentence
            else:
                chunk += '. ' + sentence if chunk else sentence
        if chunk:
            chunks.append(chunk.strip())
        return chunks
    
    def generate_audio(self, text: str, output_path: str) -> bool:
        voice_id = self.get_voice()
        if not voice_id:
            raise Exception("No voice available")
        
        print("🎵 Generating audio...")
        chunks = self.chunk_text(text)
        audio_data = b""
        
        for i, chunk in enumerate(chunks, 1):
            print(f"   🔊 Chunk {i}/{len(chunks)}")
            response = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=chunk,
                model_id="eleven_monolingual_v1",
                voice_settings={
                    "stability": 0.75,
                    "similarity_boost": 0.85,
                    "style": 0.0,
                    "use_speaker_boost": True
                },
                optimize_streaming_latency=0,  # Added required parameter
                output_format="mp3_44100_128"  # Added required parameter
            )
            
            for block in response:
                audio_data += block
            time.sleep(1)  # avoid rate limit
        
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0