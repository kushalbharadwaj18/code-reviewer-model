# import requests
# import os

# class AICodeReviewer:
#     def __init__(self):
#         # ⚠️ For testing only — move to env variable in production
#         self.api_key = "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"

#         self.model_name = os.environ.get(
#             "OPENROUTER_MODEL",
#             "nvidia/nemotron-nano-12b-v2-vl:free"
#         )

#         if not self.api_key:
#             raise ValueError("OPENROUTER_API_KEY not set")

#     def review_code(self, code, language="general"):
#         if not code or len(code.strip()) < 20:
#             return "Code snippet is too short or incomplete for a meaningful review."

#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.api_key}",
#             "HTTP-Referer": "http://localhost:5000",
#             "X-Title": "AI Code Reviewer"
#         }

#         prompt = f"""
# You are a senior software engineer and expert code reviewer.

# Review the following {language} code EVEN IF IT IS INCOMPLETE.
# DO NOT ask for more code.

# Provide:
# 1. Bugs or logical errors
# 2. Missing or incomplete parts
# 3. Security issues
# 4. Performance improvements
# 5. Code style and best practices
# 6. Suggestions for improvement
# 7. Corrected code block if applicable

# Code:
# ```{language}
# {code}
# ```
# """

#         payload = {
#             "model": self.model_name,
#             "messages": [
#                 {
#                     "role": "system",
#                     "content": "You are an expert AI code reviewer."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         }

#         try:
#             response = requests.post(
#                 "https://openrouter.ai/api/v1/chat/completions",
#                 headers=headers,
#                 json=payload,
#                 timeout=30
#             )
#             response.raise_for_status()

#             return response.json()["choices"][0]["message"]["content"]

#         except Exception as e:
#             return f"API Error: {str(e)}"













import requests
import os
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
# =========================
# AI CODE REVIEWER
# =========================

class AICodeReviewer:
    def __init__(self):
        # ⚠️ FOR TESTING ONLY — move to ENV in production
        self.api_key = os.environ.get("OPENROUTER_API_KEY")

        self.model_name = os.environ.get("OPENROUTER_MODEL")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")

    def review_code(self, code, language="general"):
        if not code or len(code.strip()) < 20:
            return {
                "review": "Code snippet is too short for a meaningful review.",
                "quality_score": 0
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "AI Code Reviewer"
        }

        prompt = f"""
You are a senior software engineer and expert code reviewer.

Review the following {language} code EVEN IF IT IS INCOMPLETE.
DO NOT ask for more code.

Return the response STRICTLY in this format:

QUALITY_SCORE: (50-100)

REVIEW:
- Bugs or logical errors
- Missing or incomplete parts
- Security issues
- Performance improvements
- Code style and best practices
- Suggestions for improvement
- Corrected code if applicable

Code:
```{language}
{code}
```
"""
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert AI code reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            content = response.json()["choices"][0]["message"]["content"]

            # Extract quality score
            score_match = re.search(r"QUALITY_SCORE:\s*(\d+)", content)
            quality_score = int(score_match.group(1)) if score_match else 5

            # Remove score from review text
            review_text = re.sub(r"QUALITY_SCORE:\s*\d", "", content).strip()
            return {
                "review": review_text,
                "quality_score": quality_score
            }

        except Exception as e:
            return {
                "review": f"API Error: {str(e)}",
                "quality_score": 0
            }
