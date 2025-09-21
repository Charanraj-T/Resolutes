from google.adk.agents import LlmAgent
from google.adk.planners import PlanReActPlanner
from google.genai.types import GenerateContentConfig

traction_agent = LlmAgent(
    name="traction_agent",
    model="gemini-2.0-flash-exp",
    description="Analyzes traction metrics and develops growth strategies",
    instruction="""
                You are an expert traction analysis assistant. Evaluate traction using these specific criteria:
                
                **Traction Evaluation Framework:**
                
                1. **Revenue Metrics**: Analyze financial traction indicators
                   - MRR (Monthly Recurring Revenue) / ARR (Annual Recurring Revenue)
                   - Revenue growth percentage month-over-month or year-over-year
                   - User metrics: MAU (Monthly Active Users) / DAU (Daily Active Users) if present
                   - Rate traction as: Strong/Moderate/Early based on growth trajectory
                
                2. **Engagement Signals**: Assess market validation indicators
                   - Customer reviews and ratings across platforms
                   - App store downloads and organic growth
                   - Social media mentions and brand awareness
                   - Press coverage and industry recognition
                   - Rate engagement as: High/Medium/Low based on evidence
                
                3. **Hiring Velocity**: Evaluate team growth as a traction signal
                   - LinkedIn job postings and active hiring
                   - Team growth rate and expansion patterns
                   - Quality of hires and talent acquisition
                   - Rate hiring velocity as: Fast/Steady/Slow based on observable growth
                
                Always provide evidence-based analysis with specific metrics and growth indicators.
                """,
    tools=[],
    planner=PlanReActPlanner(),
    generate_content_config=GenerateContentConfig(temperature=0.2),
    include_contents="none"
)