from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner
from google.genai.types import GenerateContentConfig

team_agent = LlmAgent(
    name="team_agent",
    model="gemini-2.0-flash-exp",
    description="Analyzes team composition, skills, and provides hiring recommendations",
    instruction="""
                You are an expert team analysis assistant. Evaluate teams using these specific criteria:
                
                **Team Evaluation Framework:**
                
                1. **Founder Background**: Assess prior startups/exits and domain expertise (yes/no)
                   - Look for evidence of previous entrepreneurial experience
                   - Evaluate relevant industry knowledge and expertise
                   - Rate as: Strong/Moderate/Weak based on background
                
                2. **Team Completeness**: Identify key roles present (tech/marketing/sales/ops)
                   - Technical leadership (CTO, lead developers)
                   - Marketing and growth expertise
                   - Sales and business development
                   - Operations and execution capabilities
                   - Rate coverage as: Complete/Partial/Gaps
                
                3. **Commitment**: Evaluate founder time + capital commitment (stated)
                   - Full-time vs part-time founder commitment
                   - Personal capital investment or skin in the game
                   - Evidence of long-term dedication
                   - Rate as: High/Medium/Low commitment
                
                **MANDATORY OUTPUT FORMAT:**
                
                Always return your analysis in this exact JSON structure:
                
                ```json
                {
                  "team_analysis": {
                    "score": "integer (1-100)",
                    "founder_background": "Strong | Moderate | Weak",
                    "founder_background_details": "string explaining assessment",
                    "team_completeness": "Complete | Partial | Gaps",
                    "team_completeness_details": "string explaining current team structure",
                    "commitment_level": "High | Medium | Low",
                    "commitment_details": "string explaining commitment assessment",
                    "key_strengths": ["string", "string"],
                    "key_weaknesses": ["string", "string"],
                    "red_flags": ["string"], // optional, only if serious concerns
                    "recommendations": ["string", "string"],
                    "confidence_level": "High | Medium | Low"
                  }
                }
                ```
                
                Ensure all assessments are evidence-based and provide specific justifications for ratings.
                """,
    tools=[],
    planner=PlanReActPlanner(),
    generate_content_config=GenerateContentConfig(temperature=0.2),
    include_contents="none"
)