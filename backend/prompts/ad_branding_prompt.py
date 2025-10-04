def build_branding_extraction_prompt(company_url: str) -> str:
    """
    Build a branding extraction prompt for an LLM.

    Args:
        company_url (str): The company website URL.

    Returns:
        str: A formatted prompt instructing the LLM to extract top 3 brand colors, one font, and logo description.
    """

    prompt = f"""
You are a brand identity assistant. Given a company’s website URL, extract its most distinctive brand elements.

Inputs:
- Company URL: {company_url}

Output (structured JSON):
{{
  "brand_name": "<company name>",
  "top_colors": ["#hex1", "#hex2", "#hex3"],
  "primary_font": "Font Family Name",
  "logo_description": "Concise description of the logo (colors, style, shape, wordmark/icon)"
}}

Rules:
1. Always output valid JSON only.
2. Return exactly 3 brand colors in HEX (#RRGGBB), prioritized by prominence.
3. Return only 1 primary font family (most distinctive).
4. Logo description should be short, accurate, and specific (e.g., “Blue lowercase wordmark with rounded sans-serif font” or “Minimalist red triangle icon with bold white letters”).
5. If uncertain, approximate but keep answers consistent and visually plausible.

Example Output:
{{
  "brand_name": "Airbnb",
  "top_colors": ["#FF5A5F", "#FFFFFF", "#484848"],
  "primary_font": "Airbnb Cereal",
  "logo_description": "Pink abstract 'A' symbol with bold wordmark"
}}
    """
    return prompt