from google import genai
import time 
from google.genai.errors import ServerError

class GeminiGenerator:
    def __init__(self, api_key):
       self.client = genai.Client(api_key = api_key)

    def generate(self,prompt, retries=3):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model = "gemini-2.5-flash",
                    contents=prompt
                )
                return response.text
            except ServerError as e:
                if "503" in str(e):
                    if attempt < retries -1:
                        time.sleep(2**attempt)
                    else:
                        raise RuntimeError("MODEL_BUSY")
            except ServerError as e:
                raise RuntimeError("GENERIC_ERROR")
