# Installation Instructions

## Install reportlab for PDF generation

Since you're on macOS with externally managed Python environment, you have several options:

### Option 1: Using virtual environment (Recommended)
```bash
cd /Users/abhishekj/Documents/GitHub/Resolutes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Option 2: Using system packages flag
```bash
python3 -m pip install reportlab --break-system-packages --user
```

### Option 3: Using Homebrew
```bash
brew install python-reportlab
```

### Option 4: Using pipx
```bash
brew install pipx
pipx install reportlab
```

## To run the application:
```bash
# If using virtual environment
source venv/bin/activate
streamlit run ui/app.py

# Or directly
streamlit run ui/app.py
```

## Features Implemented:

**PDF Report Generation**
- Professional investment-grade PDF reports
- Comprehensive analysis sections
- Tables and formatted content
- Download functionality
- In-browser PDF preview

**JSON Data Parsing**
- Handles all analysis types (team, market, product, traction, finance, competitor)
- Graceful handling of missing or unavailable data
- Proper formatting and structure

**UI Integration**
- Download button for PDF reports
- In-browser PDF viewing
- Progress indicators
- Error handling and user feedback

The system is now ready to generate professional investment reports from your ADK analysis data!