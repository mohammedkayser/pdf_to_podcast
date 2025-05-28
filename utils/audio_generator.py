import os
from gtts import gTTS

class AudioGenerator:
    def __init__(self):
        pass

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
        print("🎵 Generating audio with gTTS...")
        chunks = self.chunk_text(text)

        try:
            full_audio = b""
            for i, chunk in enumerate(chunks, 1):
                print(f"   🔊 Chunk {i}/{len(chunks)}")
                tts = gTTS(text=chunk, lang='en')
                chunk_path = f"{output_path}_chunk_{i}.mp3"
                tts.save(chunk_path)
                with open(chunk_path, "rb") as cf:
                    full_audio += cf.read()
                os.remove(chunk_path)

            with open(output_path, "wb") as f:
                f.write(full_audio)

            return os.path.exists(output_path) and os.path.getsize(output_path) > 0

        except Exception as e:
            print(f"❌ Failed to generate audio: {e}")
            return False
