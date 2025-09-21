import json
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

class InvestmentReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the report"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        )
        
        # Subsection style
        self.subsection_style = ParagraphStyle(
            'SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.blue
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Metrics style
        self.metrics_style = ParagraphStyle(
            'Metrics',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=4
        )

    def safe_get(self, data, key, default="Not Available"):
        """Safely get data from nested dictionaries"""
        if isinstance(data, dict):
            return data.get(key, default)
        return default

    def format_list_items(self, items, default="No data available"):
        """Format list items for display"""
        if not items or items == ["string"] or items == []:
            return default
        if isinstance(items, list):
            formatted_items = []
            for item in items:
                if item and item != "string" and item != "Not Available":
                    formatted_items.append(f"• {item}")
            return "\n".join(formatted_items) if formatted_items else default
        return str(items)

    def create_executive_summary_page(self, data):
        """Create executive summary page"""
        story = []
        
        # Title
        company_name = self.safe_get(data.get('analysis_metadata', {}), 'company_name', 'Company Analysis')
        story.append(Paragraph(f"Investment Analysis Report", self.title_style))
        story.append(Paragraph(f"{company_name}", self.section_style))
        story.append(Spacer(1, 20))
        
        # Analysis metadata
        metadata = data.get('analysis_metadata', {})
        story.append(Paragraph("Analysis Overview", self.subsection_style))
        
        metadata_table = [
            ['Analysis Date:', self.safe_get(metadata, 'analysis_date')],
            ['Analysis Type:', self.safe_get(metadata, 'analysis_type')],
            ['Confidence Level:', self.safe_get(metadata, 'confidence_level')],
            ['Data Sources:', ', '.join(metadata.get('data_sources', []))]
        ]
        
        table = Table(metadata_table, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Investment Summary
        investment_summary = data.get('investment_summary', {})
        if investment_summary and investment_summary != {}:
            story.append(Paragraph("Investment Summary", self.section_style))
            
            # Key metrics table
            key_metrics = [
                ['Overall Score:', f"{self.safe_get(investment_summary, 'overall_score')}/10"],
                ['Recommendation:', self.safe_get(investment_summary, 'investment_recommendation')],
                ['Investment Thesis:', self.safe_get(investment_summary, 'investment_thesis')]
            ]
            
            metrics_table = Table(key_metrics, colWidths=[2*inch, 4*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 15))
            
            # Key strengths and risks
            story.append(Paragraph("Key Strengths:", self.subsection_style))
            strengths = self.format_list_items(investment_summary.get('key_strengths', []))
            story.append(Paragraph(strengths, self.body_style))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("Key Risks:", self.subsection_style))
            risks = self.format_list_items(investment_summary.get('key_risks', []))
            story.append(Paragraph(risks, self.body_style))
        
        # Executive Summary
        exec_summary = data.get('executive_summary', {})
        if exec_summary and exec_summary != {}:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Executive Summary", self.section_style))
            
            for key, label in [
                ('business_model_summary', 'Business Model'),
                ('market_opportunity', 'Market Opportunity'),
                ('competitive_position', 'Competitive Position'),
                ('financial_outlook', 'Financial Outlook'),
                ('team_assessment', 'Team Assessment')
            ]:
                value = self.safe_get(exec_summary, key)
                if value and value != "Not Available":
                    story.append(Paragraph(f"{label}:", self.subsection_style))
                    story.append(Paragraph(value, self.body_style))
                    story.append(Spacer(1, 8))
        
        story.append(PageBreak())
        return story

    def create_team_analysis_page(self, team_data):
        """Create team analysis page"""
        story = []
        story.append(Paragraph("Team Analysis", self.section_style))
        
        if not team_data or team_data == {}:
            story.append(Paragraph("Team analysis data not available.", self.body_style))
            story.append(PageBreak())
            return story
        
        # Team summary
        team_summary = team_data.get('team_summary', {})
        if team_summary:
            summary_data = [
                ['Analysis Date:', self.safe_get(team_summary, 'analysis_date')],
                ['Confidence Level:', self.safe_get(team_summary, 'confidence_level')],
                ['Research Depth:', self.safe_get(team_summary, 'research_depth')]
            ]
            
            table = Table(summary_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 10)
            ]))
            story.append(table)
            story.append(Spacer(1, 15))
        
        # Founding team
        founding_team = team_data.get('founding_team', {})
        if founding_team:
            story.append(Paragraph("Founding Team", self.subsection_style))
            
            founders = founding_team.get('founders', [])
            if founders and founders != [{"name": "string"}] and len(founders) > 0:
                for founder in founders:
                    if isinstance(founder, dict) and founder.get('name', '') != 'string':
                        name = self.safe_get(founder, 'name')
                        role = self.safe_get(founder, 'role')
                        if name != "Not Available" and role != "Not Available":
                            story.append(Paragraph(f"<b>{name}</b> - {role}", self.body_style))
                            
                            background = self.safe_get(founder, 'background')
                            if background != "Not Available":
                                story.append(Paragraph(f"Background: {background}", self.metrics_style))
                            
                            experience = self.safe_get(founder, 'previous_experience')
                            if experience != "Not Available":
                                story.append(Paragraph(f"Experience: {experience}", self.metrics_style))
                            story.append(Spacer(1, 8))
            else:
                story.append(Paragraph("Founder information not available in public sources.", self.body_style))
        
        # Team assessment
        team_assessment = team_data.get('team_assessment', {})
        if team_assessment:
            story.append(Paragraph("Team Assessment", self.subsection_style))
            
            assessment_data = []
            for key, label in [
                ('founder_market_fit', 'Founder-Market Fit'),
                ('execution_capability', 'Execution Capability'),
                ('technical_competency', 'Technical Competency'),
                ('business_acumen', 'Business Acumen'),
                ('scaling_readiness', 'Scaling Readiness')
            ]:
                value = self.safe_get(team_assessment, key)
                if value != "Not Available":
                    assessment_data.append([f"{label}:", value])
            
            if assessment_data:
                assessment_table = Table(assessment_data, colWidths=[2.5*inch, 1.5*inch])
                assessment_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(assessment_table)
        
        story.append(PageBreak())
        return story

    def create_market_analysis_page(self, market_data):
        """Create market analysis page"""
        story = []
        story.append(Paragraph("Market Analysis", self.section_style))
        
        if not market_data or market_data == {}:
            story.append(Paragraph("Market analysis data not available.", self.body_style))
            story.append(PageBreak())
            return story
        
        # Market size
        market_size = market_data.get('market_size', {})
        if market_size:
            story.append(Paragraph("Market Sizing", self.subsection_style))
            
            market_data_table = []
            for key, label in [
                ('total_addressable_market', 'Total Addressable Market (TAM):'),
                ('serviceable_addressable_market', 'Serviceable Addressable Market (SAM):'),
                ('market_growth_rate', 'Market Growth Rate:'),
                ('market_maturity', 'Market Maturity:')
            ]:
                value = self.safe_get(market_size, key)
                if value != "Not Available":
                    market_data_table.append([label, value])
            
            if market_data_table:
                table = Table(market_data_table, colWidths=[2.5*inch, 3.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(table)
                story.append(Spacer(1, 15))
        
        # Competitive landscape
        competitive = market_data.get('competitive_landscape', {})
        if competitive:
            story.append(Paragraph("Competitive Landscape", self.subsection_style))
            
            # Direct competitors
            direct_competitors = competitive.get('direct_competitors', [])
            if direct_competitors and direct_competitors != [{"name": "string"}] and len(direct_competitors) > 0:
                story.append(Paragraph("Direct Competitors:", self.body_style))
                for competitor in direct_competitors:
                    if isinstance(competitor, dict) and competitor.get('name', '') != 'string':
                        comp_name = self.safe_get(competitor, 'name')
                        market_share = self.safe_get(competitor, 'market_share')
                        if comp_name != "Not Available":
                            story.append(Paragraph(f"• {comp_name} (Market Share: {market_share})", self.metrics_style))
            else:
                story.append(Paragraph("Competitive information not available in public sources.", self.body_style))
        
        # Market opportunity
        opportunity = market_data.get('market_opportunity', {})
        if opportunity:
            story.append(Spacer(1, 15))
            story.append(Paragraph("Market Opportunity Assessment", self.subsection_style))
            
            opp_data = []
            for key, label in [
                ('market_timing', 'Market Timing'),
                ('growth_potential', 'Growth Potential'),
                ('competitive_advantage_potential', 'Competitive Advantage Potential'),
                ('market_accessibility', 'Market Accessibility')
            ]:
                value = self.safe_get(opportunity, key)
                if value != "Not Available":
                    opp_data.append([f"{label}:", value])
            
            if opp_data:
                opp_table = Table(opp_data, colWidths=[2.5*inch, 1.5*inch])
                opp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(opp_table)
        
        story.append(PageBreak())
        return story

    def create_financial_analysis_page(self, financial_data):
        """Create financial analysis page"""
        story = []
        story.append(Paragraph("Financial Analysis", self.section_style))
        
        if not financial_data or financial_data == {}:
            story.append(Paragraph("Financial analysis data not available.", self.body_style))
            story.append(PageBreak())
            return story
        
        # Funding history
        funding = financial_data.get('funding_history', {})
        if funding:
            story.append(Paragraph("Funding History", self.subsection_style))
            
            funding_data = []
            for key, label in [
                ('total_funding_raised', 'Total Funding Raised:'),
                ('number_of_rounds', 'Number of Rounds:'),
                ('latest_valuation', 'Latest Valuation:'),
                ('funding_trajectory', 'Funding Trajectory:')
            ]:
                value = self.safe_get(funding, key)
                if value != "Not Available":
                    if key == 'number_of_rounds':
                        value = str(value)
                    funding_data.append([label, value])
            
            if funding_data:
                table = Table(funding_data, colWidths=[2*inch, 4*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(table)
                story.append(Spacer(1, 15))
        
        # Business model
        business_model = financial_data.get('business_model', {})
        if business_model:
            story.append(Paragraph("Business Model", self.subsection_style))
            
            revenue_model = self.safe_get(business_model, 'revenue_model')
            if revenue_model != "Not Available":
                story.append(Paragraph(f"Revenue Model: {revenue_model}", self.body_style))
            
            pricing_model = self.safe_get(business_model, 'pricing_model')
            if pricing_model != "Not Available":
                story.append(Paragraph(f"Pricing Model: {pricing_model}", self.body_style))
            
            # Unit economics
            unit_economics = business_model.get('unit_economics', {})
            if unit_economics:
                story.append(Paragraph("Unit Economics:", self.subsection_style))
                unit_data = []
                for key, label in [
                    ('customer_acquisition_cost', 'Customer Acquisition Cost:'),
                    ('customer_lifetime_value', 'Customer Lifetime Value:'),
                    ('gross_margin', 'Gross Margin:'),
                    ('payback_period', 'Payback Period:')
                ]:
                    value = self.safe_get(unit_economics, key)
                    if value != "Not Available":
                        unit_data.append([label, value])
                
                if unit_data:
                    unit_table = Table(unit_data, colWidths=[2.5*inch, 2*inch])
                    unit_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (-1, -1), 10)
                    ]))
                    story.append(unit_table)
        
        story.append(PageBreak())
        return story

    def create_product_analysis_page(self, product_data):
        """Create product analysis page"""
        story = []
        story.append(Paragraph("Product Analysis", self.section_style))
        
        if not product_data or product_data == {}:
            story.append(Paragraph("Product analysis data not available.", self.body_style))
            story.append(PageBreak())
            return story
        
        # Product overview
        overview = product_data.get('product_overview', {})
        if overview:
            story.append(Paragraph("Product Overview", self.subsection_style))
            
            overview_data = []
            for key, label in [
                ('product_name', 'Product Name:'),
                ('product_category', 'Category:'),
                ('primary_value_proposition', 'Value Proposition:'),
                ('launch_date', 'Launch Date:')
            ]:
                value = self.safe_get(overview, key)
                if value != "Not Available":
                    overview_data.append([label, value])
            
            if overview_data:
                table = Table(overview_data, colWidths=[2*inch, 4*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(table)
                story.append(Spacer(1, 15))
        
        # Core features
        features = product_data.get('core_features', {})
        if features:
            story.append(Paragraph("Core Features Assessment", self.subsection_style))
            
            feature_data = []
            for key, label in [
                ('feature_completeness', 'Feature Completeness:'),
                ('unique_differentiators', 'Unique Differentiators:')
            ]:
                value = self.safe_get(features, key)
                if value != "Not Available":
                    if isinstance(value, list):
                        value = ', '.join([item for item in value if item and item != "string"])
                    feature_data.append([label, value])
            
            if feature_data:
                feature_table = Table(feature_data, colWidths=[2*inch, 4*inch])
                feature_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightcyan),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(feature_table)
        
        story.append(PageBreak())
        return story

    def create_traction_analysis_page(self, traction_data):
        """Create traction analysis page"""
        story = []
        story.append(Paragraph("Traction Analysis", self.section_style))
        
        if not traction_data or traction_data == {}:
            story.append(Paragraph("Traction analysis data not available.", self.body_style))
            story.append(PageBreak())
            return story
        
        # Growth metrics
        growth_metrics = traction_data.get('growth_metrics', {})
        if growth_metrics:
            story.append(Paragraph("Growth Metrics", self.subsection_style))
            
            # User growth
            user_growth = growth_metrics.get('user_growth', {})
            if user_growth:
                user_data = []
                for key, label in [
                    ('total_users', 'Total Users:'),
                    ('growth_rate', 'Growth Rate:'),
                    ('user_acquisition_trend', 'Acquisition Trend:')
                ]:
                    value = self.safe_get(user_growth, key)
                    if value != "Not Available":
                        user_data.append([label, value])
                
                if user_data:
                    user_table = Table(user_data, colWidths=[2*inch, 3*inch])
                    user_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (-1, -1), 10)
                    ]))
                    story.append(user_table)
                    story.append(Spacer(1, 10))
        
        # Traction assessment
        assessment = traction_data.get('traction_assessment', {})
        if assessment:
            story.append(Paragraph("Traction Assessment", self.subsection_style))
            
            assessment_data = []
            for key, label in [
                ('overall_momentum', 'Overall Momentum:'),
                ('growth_sustainability', 'Growth Sustainability:'),
                ('market_validation_strength', 'Market Validation:'),
                ('execution_capability', 'Execution Capability:')
            ]:
                value = self.safe_get(assessment, key)
                if value != "Not Available":
                    assessment_data.append([label, value])
            
            if assessment_data:
                assessment_table = Table(assessment_data, colWidths=[2.5*inch, 1.5*inch])
                assessment_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 10)
                ]))
                story.append(assessment_table)
        
        story.append(PageBreak())
        return story

    def create_competitive_analysis_page(self, competitive_data):
        """Create competitive analysis page"""
        story = []
        story.append(Paragraph("Competitive Analysis", self.section_style))
        
        if not competitive_data or competitive_data == {}:
            story.append(Paragraph("Competitive analysis data not available.", self.body_style))
            story.append(PageBreak())
            return story
        
        # Company overview
        company_name = self.safe_get(competitive_data, 'company_name')
        sector = self.safe_get(competitive_data, 'sector')
        
        story.append(Paragraph(f"Target Company: {company_name}", self.subsection_style))
        story.append(Paragraph(f"Sector: {sector}", self.body_style))
        story.append(Spacer(1, 15))
        
        # Competitors
        competitors = competitive_data.get('competitors', [])
        if competitors and len(competitors) > 0:
            story.append(Paragraph("Key Competitors", self.subsection_style))
            
            for competitor in competitors:
                if isinstance(competitor, dict):
                    comp_name = self.safe_get(competitor, 'company_name')
                    if comp_name != "Not Available":
                        story.append(Paragraph(f"<b>{comp_name}</b>", self.body_style))
                        
                        # Competitor details
                        details = []
                        for key, label in [
                            ('founding_year', 'Founded:'),
                            ('total_funding_raised', 'Funding:'),
                            ('business_model', 'Business Model:')
                        ]:
                            value = self.safe_get(competitor, key)
                            if value != "Not Available":
                                details.append(f"{label} {value}")
                        
                        if details:
                            story.append(Paragraph(" | ".join(details), self.metrics_style))
                        story.append(Spacer(1, 8))
        
        # Competitive summary
        comp_summary = competitive_data.get('competitive_summary', {})
        if comp_summary:
            story.append(Paragraph("Competitive Summary", self.subsection_style))
            
            positioning = self.safe_get(comp_summary, 'positioning_vs_competition')
            if positioning != "Not Available":
                story.append(Paragraph(f"Market Positioning: {positioning}", self.body_style))
                story.append(Spacer(1, 8))
            
            moat = self.safe_get(comp_summary, 'competitive_moat_assessment')
            if moat != "Not Available":
                story.append(Paragraph(f"Competitive Moat: {moat}", self.body_style))
        
        story.append(PageBreak())
        return story

    def generate_pdf(self, analysis_data, startup_name):
        """Generate the complete PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
        
        story = []
        
        # Parse JSON if it's a string
        if isinstance(analysis_data, str):
            try:
                analysis_data = json.loads(analysis_data)
            except json.JSONDecodeError:
                # If parsing fails, create a basic error report
                story.append(Paragraph("Analysis Report Generation Error", self.title_style))
                story.append(Paragraph("Unable to parse analysis data. Raw response:", self.section_style))
                story.append(Paragraph(str(analysis_data), self.body_style))
                doc.build(story)
                buffer.seek(0)
                return buffer
        
        # Create all sections
        story.extend(self.create_executive_summary_page(analysis_data))
        story.extend(self.create_team_analysis_page(analysis_data.get('team_analysis', {})))
        story.extend(self.create_market_analysis_page(analysis_data.get('market_analysis', {})))
        story.extend(self.create_product_analysis_page(analysis_data.get('product_analysis', {})))
        story.extend(self.create_traction_analysis_page(analysis_data.get('traction_analysis', {})))
        story.extend(self.create_financial_analysis_page(analysis_data.get('financial_analysis', {})))
        story.extend(self.create_competitive_analysis_page(analysis_data.get('competitive_analysis', {})))
        
        # Build the PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

def generate_investment_report_pdf(analysis_data, startup_name):
    """Main function to generate investment report PDF"""
    generator = InvestmentReportGenerator()
    return generator.generate_pdf(analysis_data, startup_name)