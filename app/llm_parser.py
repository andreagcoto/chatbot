# app/llm_parser.py

import json
import re
import ollama

SYSTEM_PROMPT = """
You extract housing features from text.
Return only valid JSON.
Allowed keys:
OverallQual, GrLivArea, TotalBsmtSF, GarageCars, YearBuilt,
LotArea, CentralAir, OverallCond, GarageType, YearRemodAdd, BsmtQual

Rules:
- OverallQual and OverallCond must be integers from 1 to 10
- CentralAir must be "Y" or "N"
- GarageType must be one of: "Attchd", "Detchd", "BuiltIn", "CarPort", "None"
- BsmtQual must be one of: "Ex", "Gd", "TA", "Fa", "Po", "None"
- Omit any feature that is not clearly supported by the text
- Return JSON only, with no explanation and no markdown
"""

def parse_house_text_with_llm(description: str, model: str = "llama3") -> dict:
    if not description.strip():
        raise ValueError("Description cannot be empty.")

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": description},
            ]
        )

        content = response["message"]["content"].strip()

        # Remove markdown fences if the model still adds them
        content = re.sub(r"```json|```", "", content).strip()

        data = json.loads(content)

        if not isinstance(data, dict):
            raise ValueError(f"LLM output is not a JSON object: {content}")

        return data

    except Exception as e:
        raise ValueError(f"Error communicating with LLM or parsing JSON: {e}")