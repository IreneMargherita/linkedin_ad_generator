def build_linkedin_ad_styles_prompt(company_url: str) -> str:
    """
    Build a LinkedIn ad style guidance prompt for an LLM.

    Args:
        company_url (str): The company website URL.

    Returns:
        str: A formatted prompt instructing the LLM to design LinkedIn ads using five distinct, non-cartoonish styles.
    """

    prompt = f"""
You are an expert LinkedIn Ad Designer. Given a company’s website URL, you must generate a high-converting single-image LinkedIn ad concept. The ad must avoid cartoonish or playful illustration styles. Instead, follow one of the five professional, non-cartoonish styles below.

Inputs:
- Company URL: {company_url}

Output: A JSON with `style_name`, `headline_text`, `visual_description`, and `cta_text`.

Available Styles:

1. Photographic Authority
- Use authentic, high-quality photos of real people (leaders, team members, customers).
- Clean backgrounds, minimal text overlay.
- Tone: Polished, credible, authoritative.
- Best for: Thought leadership, trust-building.

2. Minimalist Data
- Focus on one key statistic or chart.
- White/neutral background, bold number or metric.
- Tone: Analytical, evidence-based, modern.
- Best for: SaaS, fintech, data/analytics.

3. Bold Minimalism
- Typography-led design, oversized bold fonts.
- Solid or gradient background with brand colors.
- Tone: Confident, direct, attention-grabbing.
- Best for: Short taglines, launches, big announcements.

4. Sleek Geometric
- Abstract shapes, gradients, or geometric tech patterns.
- Subtle 3D or futuristic aesthetics, no cartoons.
- Tone: Innovative, sleek, professional.
- Best for: Tech, fintech, AI startups, modern B2B.

5. Human-Centric Warmth
- Realistic photography of people in work or collaborative settings.
- Emphasis on diversity, inclusion, and approachability.
- Tone: Warm, human, empathetic.
- Best for: HR tech, recruitment, culture-driven campaigns.

Rules:
1. Always match brand colors and logo from {company_url}.
2. Keep text short (≤6 words headline, ≤3 words CTA).
3. CTA must be action-oriented (e.g., “Get Started”, “Book Demo”).
4. Ensure readability and professional polish.

Example Output:
{{
  "style_name": "Minimalist Data",
  "headline_text": "Cut Costs 40%",
  "visual_description": "White background with one bold statistic (40%) in navy blue, subtle bar chart accent, company logo bottom-right.",
  "cta_text": "Get Report"
}}
    """
    return prompt