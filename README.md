# Spana - AI-Powered Brainstorming Assistant

## Overview

Spana is a web application that leverages Google's Gemini AI to enhance brainstorming sessions by applying structured thinking techniques and diverse perspectives from business icons. It helps teams move beyond uninspired sessions and pushes thinking into new directions while maintaining focus on core problems.

## Features

- **Multiple Brainstorming Techniques**: Choose from 8 proven methodologies
  - 5 Whys
  - Starbursting
  - SWOT Analysis
  - Porter's 5 Forces
  - Six Thinking Hats
  - SCAMPER
  - Charrette
  - Stepladder

- **Industry Context**: Optional business area selection for tailored insights
- **Icon Perspectives**: Apply thinking styles of legendary business leaders and innovators
- **AI-Generated Output**: Structured markdown responses from Gemini AI
- **Professional Interface**: Clean, navy blue design with Segoe UI/Helvetica fonts

## File Structure

```
spana/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── vercel.json                # Vercel deployment configuration
├── README.md                  # This file
│
├── templates/
│   ├── index.html             # Landing page
│   └── app.html               # Main application interface
│
└── static/
    ├── css/
    │   └── style.css          # Global styles
    ├── js/
    │   └── app.js             # Frontend JavaScript
    └── images/
        └── (optional assets)
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- pip (Python package manager)

## Installation

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

   Or set environment variables directly:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   export FLASK_SECRET_KEY="your_secret_key_here"
   ```

## Running the Application

### Local Development

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Deployment (Vercel)

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Set environment variables in Vercel dashboard:
   - `GEMINI_API_KEY`
   - `FLASK_SECRET_KEY`

## Usage Guide

### Landing Page
1. Navigate to the home page
2. Read about Spana's capabilities
3. Click "Launch Spana" to access the application

### Application Page

1. **Select Brainstorming Technique** (Required)
   - Choose from 8 proven methodologies

2. **Select Business Area** (Optional)
   - Pick an industry for contextualized insights

3. **Select Business Icon** (Optional)
   - Apply the perspective of a legendary leader or innovator

4. **Enter Issue and Expectations** (Required)
   - Describe the problem you're trying to solve
   - Include what you hope to achieve

5. **Enter Assumptions** (Optional)
   - List any constraints, facts, or givens

6. **Generate Output**
   - Click the generate button
   - View AI-generated brainstorming content in markdown format

## API Integration

Spana uses Google's Gemini API to generate responses. The application constructs prompts based on:
- Selected brainstorming technique
- Business area context
- Business icon perspective
- User's issue description
- Stated assumptions

## Dependencies

- Flask: Web framework
- google-generativeai: Gemini AI integration
- python-dotenv: Environment variable management
- markdown2: Markdown rendering (optional)

## Security Considerations

- Never commit `.env` files to version control
- Keep API keys secure
- Use environment variables for sensitive data
- Implement rate limiting for production use
- Add CSRF protection for forms

## Customization

### Styling
- Edit `static/css/style.css` to modify the navy blue theme
- Font stack: Segoe UI, Helvetica, Arial, sans-serif

### Techniques/Icons
- Modify arrays in `templates/app.html` to add/remove options
- Update prompt construction in `app.py` for new techniques

## Troubleshooting

**API Key Issues**
- Verify your Gemini API key is valid
- Check environment variable is set correctly
- Ensure API quota is not exceeded

**Port Already in Use**
- Change port in `app.py`: `app.run(port=5001)`

**Template Not Found**
- Ensure `templates/` directory exists
- Verify HTML files are named correctly

## Future Enhancements
- User authentication and session management
- Save brainstorming sessions
- Export to PDF/DOCX
- Collaborative sessions
- Custom technique creation
- Analytics and insights
- Add more brainstorming techniques
- Potentially build it into a full-scale productivity app

## Acknowledgments

- Google Gemini AI for powering the brainstorming engine
- Flask community for the excellent web framework
