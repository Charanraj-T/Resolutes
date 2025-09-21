import datetime
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai.types import GenerateContentConfig
from .subagents import (
    team_agent,
    market_agent,
    product_agent,
    traction_agent,
    finance_agent,
    competitor_agent
)

# STEP 1: A Parallel Agent to run all research-enabled specialist analyses simultaneously.
# Each agent conducts its own independent research and analysis.
parallel_research_analysis = ParallelAgent(
    name="parallel_research_analysis",
    description="Runs all research-enabled specialist agents in parallel to gather independent analysis reports.",
    sub_agents=[
        team_agent,
        market_agent,
        product_agent,
        traction_agent,
        finance_agent,
        competitor_agent,
    ],
)

# STEP 2: A Final Synthesizer Agent to assemble the complete report.
# This agent takes the outputs from all parallel agents and builds the final JSON.
final_synthesizer = LlmAgent(
    name="final_report_synthesizer",
    model="gemini-2.5-pro",
    description="Synthesizes individual research-backed analysis reports into a single, comprehensive JSON output.",
    instruction=f"""
        You are "Resolutes ADK", the final synthesizer. Your job is to assemble the individual JSON reports from 6 research-enabled specialist agents into one comprehensive final report.

        **AVAILABLE DATA:**
        You have access to the outputs from the following research-enabled agents. The data is available in state keys corresponding to the agent names.

        1. `team_agent`: Provides research-backed `team_analysis`
        2. `market_agent`: Provides research-backed `market_analysis`
        3. `product_agent`: Provides research-backed `product_analysis`
        4. `traction_agent`: Provides research-backed `traction_analysis`
        5. `finance_agent`: Provides research-backed `financial_analysis`
        6. `competitor_agent`: Provides research-backed `competitive_analysis`

        **YOUR TASK:**
        1.  **Combine Data**: Take the JSON output from each of the 7 agents.
        2.  **Generate Summaries**: Based on the combined data, create the `investment_summary` and `executive_summary` sections.
        3.  **Build Final JSON**: Assemble everything into the final, large JSON structure below. Ensure every field is present.

        **FINAL OUTPUT JSON STRUCTURE:**
        ```json
        {{
          "analysis_metadata": {{
            "company_name": "string (extract from agent data)",
            "analysis_date": "{datetime.date.today().isoformat()}",
            "analysis_type": "comprehensive_research_backed",
            "confidence_level": "High",
            "data_sources": ["team_agent", "market_agent", "product_agent", "traction_agent", "finance_agent", "competitor_agent"]
          }},
          "team_analysis": {{
            // **INSERT COMPLETE JSON FROM `team_agent` HERE**
          }},
          "market_analysis": {{
            // **INSERT COMPLETE JSON FROM `market_agent` HERE**
          }},
          "product_analysis": {{
            // **INSERT COMPLETE JSON FROM `product_agent` HERE**
          }},
          "traction_analysis": {{
            // **INSERT COMPLETE JSON FROM `traction_agent` HERE**
          }},
          "financial_analysis": {{
            // **INSERT COMPLETE JSON FROM `finance_agent` HERE**
          }},
          "competitive_analysis": {{
            // **INSERT COMPLETE JSON FROM `competitor_agent` HERE**
          }},
          "investment_summary": {{
            "overall_score": "number (1-10, your synthesis)",
            "investment_recommendation": "Strong Buy|Buy|Hold|Pass (your synthesis)",
            "key_strengths": ["string (your synthesis)"],
            "key_risks": ["string (your synthesis)"],
            "critical_next_steps": ["string (your synthesis)"],
            "comparable_valuations": {{
              "estimated_valuation_range": "string (your synthesis)",
              "valuation_methodology": "string (your synthesis)",
              "peer_multiples": "string (your synthesis)"
            }},
            "investment_thesis": "string (2-3 sentences, your synthesis)",
            "due_diligence_priorities": ["string (your synthesis)"]
          }},
          "executive_summary": {{
            "business_model_summary": "string (your synthesis)",
            "market_opportunity": "string (your synthesis)",
            "competitive_position": "string (your synthesis)",
            "financial_outlook": "string (your synthesis)",
            "team_assessment": "string (your synthesis)",
            "investment_highlights": ["string (your synthesis)"],
            "risk_factors": ["string (your synthesis)"]
          }}
        }}
        ```
    """,
    generate_content_config=GenerateContentConfig(
        temperature=0.2, response_mime_type="application/json"
    ),
)


# The Root Agent is now a Sequential pipeline with research-enabled specialists.
root_agent = SequentialAgent(
    name="research_backed_analysis_pipeline",
    description="A sequential pipeline that runs parallel research-enabled analyses and then synthesizes results into a final investment report.",
    sub_agents=[
        parallel_research_analysis,
        final_synthesizer,
    ],
)