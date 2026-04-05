# prompts.py

# This is a standard Python dictionary (like a JS object)
PROMPTS = {
    "parser":"""
You are extracting structured data from a New York City Transit General Order document.

These documents are semi-structured and may contain OCR noise, line breaks, and inconsistent formatting.
You must normalize and clean the data.

====================
DOCUMENT TEXT
====================
{text}

====================
OUTPUT FORMAT
====================
Return STRICT JSON with the following schema:

{{
  "general_order": string,
  "app": string,
  "sub_division": string,
  "lines": string[],
  "tracks": number[],
  "start_datetime": string,
  "end_datetime": string,
  "duration_hours": number,
  "purpose": string,
  "works_with": string[],
  "affected_service": string
}}

====================
EXTRACTION RULES
====================

GENERAL:
- Return ONLY valid JSON (no markdown, no explanation)
- Remove all OCR noise, headers, footers, page numbers
- Combine multi-line fields into clean values
- If a value is missing, return null

GENERAL ORDER:
- Must match format ####-## (example: 4101-26)
- Do NOT include words like "No." or "GENERAL ORDER"

APP:
- Format: Letter-Number-Number (example: B-03-60)
- Extract only the value, no labels

SUBDIVISION:
- Single uppercase letter (example: "B")

LINES:
- Extract subway lines, it includes letters and also full names like Eastern Parkway Line, 7 Avenue Line etc. (example: ["J", "7 Avenue"], ["A","C", "Eastern Parkway"],  )
- All the lines will be mentioned in the header above the tracks in the first 30-40 lines.
- Remove Line from the name

TRACKS:
- could be just integers or letter+integers or could be letter+number/number like C2, J1, J3/4
- Find tracks from the heading "Track out of service"
- Deduplicate and sort ascending

TIMES:
- Extract start_datetime and end_datetime from "Times and Dates" section
- Preserve original meaning even if formatting is messy

DURATION:
- duration_hours must be a number (e.g. 53)
- Extract from phrases like "(53 continuous hours)"

PURPOSE:
- Extract full purpose description
- Combine multi-line text into ONE clean paragraph
- Remove labels like "Purpose :"

WORKS_WITH:
- Extract all referenced General Orders
- Must match format ####-##
- Return as array of strings (example: ["4100-26","4102-26"])

AFFECTED_SERVICE:
- Extract full affected service description
- Combine into clean readable text
- Remove excessive line breaks

====================
IMPORTANT
====================
- Be precise and deterministic
- Prefer correct structured output over copying raw text
- Do not hallucinate values
- If uncertain, extract best possible answer from context

Return ONLY JSON.
"""
}