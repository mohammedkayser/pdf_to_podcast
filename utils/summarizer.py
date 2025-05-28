import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PodcastScriptGenerator:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def analyze_text_length(self, text):
        return {
            "word_count": len(text.split()),
            "char_count": len(text),
            "estimated_reading_time": len(text.split()) / 200
        }

    def create_prompt(self, text, analysis):
        return f"""
You are a podcast scriptwriter. Write a natural, engaging, and easy-to-understand narration script 
based entirely on the following research paper content. Do not include host introductions, music cues, or scene directions. 
Write the content in clean, plain English like a single narrator is explaining it smoothly. 
Use proper punctuation to guide a natural voiceover. Avoid technical terms unless needed, and explain concepts clearly.

Start directly with the content, avoid any phrases like 'welcome', 'host', 'music', or 'let's begin'. 
Just produce a structured, clear summary suitable for being read aloud in a podcast.

RESEARCH PAPER TEXT:
{text}
"""

    def generate_script(self, text: str) -> str:
        analysis = self.analyze_text_length(text)
        prompt = self.create_prompt(text, analysis)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=8192
            )
        )
        return response.text
