#!/usr/bin/env python3
"""
Test script for PDF generation functionality
"""

import sys
import os
import json

# Add the utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui', 'utils'))

# Test data structure matching your ADK output format
test_analysis_data = {
    "analysis_metadata": {
        "company_name": "TestStartup Inc.",
        "analysis_date": "2025-09-21",
        "analysis_type": "comprehensive_research_backed",
        "confidence_level": "High",
        "data_sources": ["team_agent", "market_agent", "product_agent", "traction_agent", "finance_agent", "competitor_agent"]
    },
    "team_analysis": {
        "team_summary": {
            "analysis_date": "2025-09-21",
            "confidence_level": "High",
            "data_sources_count": "5",
            "research_depth": "comprehensive"
        },
        "founding_team": {
            "founders": [
                {
                    "name": "John Doe",
                    "role": "CEO",
                    "background": "Former VP of Engineering at Google",
                    "previous_experience": "15 years in tech leadership",
                    "education": "MIT Computer Science",
                    "domain_expertise": "AI/ML and enterprise software",
                    "linkedin_url": "https://linkedin.com/in/johndoe"
                }
            ],
            "founding_date": "2023-01-15",
            "team_size_at_founding": 3,
            "founder_commitment": "Full-time"
        },
        "team_assessment": {
            "founder_market_fit": "Strong",
            "execution_capability": "High",
            "technical_competency": "High",
            "business_acumen": "High",
            "team_cohesion": "Strong",
            "scaling_readiness": "Ready"
        }
    },
    "market_analysis": {
        "market_summary": {
            "analysis_date": "2025-09-21",
            "confidence_level": "High",
            "data_sources_count": "8",
            "research_depth": "comprehensive"
        },
        "market_size": {
            "total_addressable_market": "$50B USD by 2028",
            "serviceable_addressable_market": "$15B USD by 2028",
            "serviceable_obtainable_market": "$500M USD by 2028",
            "market_growth_rate": "25% CAGR 2024-2028",
            "market_maturity": "Growing"
        },
        "market_opportunity": {
            "market_timing": "Excellent",
            "growth_potential": "High",
            "competitive_advantage_potential": "Strong",
            "customer_demand_validation": "Strong",
            "market_accessibility": "Moderate"
        }
    },
    "product_analysis": {
        "product_summary": {
            "analysis_date": "2025-09-21",
            "confidence_level": "High",
            "data_sources_count": "6",
            "research_depth": "comprehensive"
        },
        "product_overview": {
            "product_name": "TestProduct AI",
            "product_category": "Enterprise AI Platform",
            "primary_value_proposition": "Automated decision making for enterprises",
            "target_users": ["Enterprise CTOs", "Data Scientists"],
            "launch_date": "2023-06-01",
            "current_version": "2.1.0"
        },
        "core_features": {
            "feature_completeness": "Mostly Complete",
            "unique_differentiators": ["Real-time AI processing", "No-code interface", "Enterprise security"]
        }
    },
    "traction_analysis": {
        "traction_summary": {
            "analysis_date": "2025-09-21",
            "confidence_level": "Medium",
            "data_sources_count": "4",
            "research_depth": "moderate"
        },
        "growth_metrics": {
            "user_growth": {
                "total_users": "50,000+",
                "growth_rate": "15% MoM",
                "growth_period": "Last 12 months",
                "user_acquisition_trend": "Accelerating"
            }
        },
        "traction_assessment": {
            "overall_momentum": "Strong",
            "growth_sustainability": "Sustainable",
            "market_validation_strength": "Strong",
            "execution_capability": "Proven"
        }
    },
    "financial_analysis": {
        "finance_summary": {
            "analysis_date": "2025-09-21",
            "confidence_level": "Medium",
            "data_sources_count": "3",
            "research_depth": "moderate"
        },
        "funding_history": {
            "total_funding_raised": "$25M USD",
            "number_of_rounds": 3,
            "latest_valuation": "$100M USD",
            "funding_trajectory": "Upward"
        },
        "business_model": {
            "revenue_model": "SaaS subscription with usage-based pricing",
            "pricing_model": "Enterprise",
            "unit_economics": {
                "customer_acquisition_cost": "$15,000",
                "customer_lifetime_value": "$180,000",
                "gross_margin": "85%",
                "payback_period": "12 months"
            }
        }
    },
    "competitive_analysis": {
        "company_name": "TestStartup Inc.",
        "sector": "Enterprise AI",
        "analysis_date": "2025-09-21",
        "competitors": [
            {
                "company_name": "CompetitorCorp",
                "headquarters": "San Francisco, USA",
                "founding_year": 2020,
                "total_funding_raised": "$75M USD",
                "business_model": "Enterprise SaaS platform for AI automation"
            }
        ],
        "competitive_summary": {
            "positioning_vs_competition": "Strong differentiation through no-code approach",
            "competitive_moat_assessment": "Strong technical moat with proprietary algorithms"
        }
    },
    "investment_summary": {
        "overall_score": 8.5,
        "investment_recommendation": "Strong Buy",
        "key_strengths": [
            "Experienced founding team with proven track record",
            "Large and growing market opportunity",
            "Strong product-market fit validation",
            "Healthy unit economics and growth metrics"
        ],
        "key_risks": [
            "Competitive market with well-funded players",
            "Dependency on continued AI/ML advancement",
            "Enterprise sales cycle complexity"
        ],
        "investment_thesis": "TestStartup represents a compelling investment opportunity in the rapidly growing enterprise AI market with experienced leadership and strong early traction.",
        "critical_next_steps": [
            "Expand enterprise sales team",
            "Develop strategic partnerships",
            "Enhance platform scalability"
        ]
    },
    "executive_summary": {
        "business_model_summary": "Enterprise AI SaaS platform targeting large organizations with no-code AI automation tools",
        "market_opportunity": "Large and growing $50B TAM in enterprise AI with 25% CAGR growth",
        "competitive_position": "Strong differentiation through no-code approach and enterprise focus",
        "financial_outlook": "Healthy unit economics with strong growth trajectory and clear path to profitability",
        "team_assessment": "Experienced founding team with proven execution capability and strong technical background"
    }
}

def test_pdf_generation():
    """Test PDF generation with sample data"""
    try:
        # Import after ensuring path is set
        from pdf_generator import generate_investment_report_pdf
        
        print("🧪 Testing PDF generation...")
        
        # Generate PDF
        pdf_buffer = generate_investment_report_pdf(test_analysis_data, "TestStartup Inc.")
        
        # Save to file for testing
        with open('test_investment_report.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print("PDF generated successfully!")
        print("Test report saved as: test_investment_report.pdf")
        print(f"PDF size: {len(pdf_buffer.getvalue())} bytes")
        
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install reportlab: pip install reportlab")
        return False
        
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return False

def test_json_parsing():
    """Test JSON parsing functionality"""
    try:
        from pdf_generator import InvestmentReportGenerator
        
        print("🧪 Testing JSON parsing...")
        
        generator = InvestmentReportGenerator()
        
        # Test with JSON string
        json_string = json.dumps(test_analysis_data)
        parsed_data = json.loads(json_string)
        
        # Test safe_get function
        company_name = generator.safe_get(parsed_data.get('analysis_metadata', {}), 'company_name')
        print(f"Company name parsed: {company_name}")
        
        # Test format_list_items function
        strengths = generator.format_list_items(
            parsed_data.get('investment_summary', {}).get('key_strengths', [])
        )
        print(f"Strengths formatted: {len(strengths)} characters")
        
        return True
        
    except Exception as e:
        print(f"JSON parsing test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting PDF Generation Tests")
    print("=" * 50)
    
    # Test JSON parsing
    json_success = test_json_parsing()
    print()
    
    # Test PDF generation
    pdf_success = test_pdf_generation()
    print()
    
    if json_success and pdf_success:
        print("All tests passed! PDF generation system is ready.")
    else:
        print("Some tests failed. Check the errors above.")
        
    print("\nNext steps:")
    print("1. Install reportlab if not already installed")
    print("2. Run the Streamlit app: streamlit run ui/app.py")
    print("3. Test with real ADK analysis data")