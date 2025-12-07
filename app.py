
import os
import json
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai.errors import APIError
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    model = None
    print("Warning: GEMINI_API_KEY not found. API calls will fail.")

# Brainstorming technique descriptions for context
TECHNIQUE_CONTEXTS = {
    '5 Whys': 'The 5 Whys technique involves asking "why" repeatedly (typically five times) to drill down to the root cause of a problem.',
    'Starbursting': 'Starbursting focuses on generating questions rather than answers, using Who, What, When, Where, Why, and How.',
    'SWOT': 'SWOT Analysis examines Strengths, Weaknesses, Opportunities, and Threats related to a business situation.',
    'Porters 5 Forces': "Porter's 5 Forces analyzes competitive rivalry, supplier power, buyer power, threat of substitution, and threat of new entry.",
    'Six Thinking Hats': 'Six Thinking Hats uses six different perspectives: White (facts), Red (emotions), Black (caution), Yellow (optimism), Green (creativity), Blue (process).',
    'SCAMPER': 'SCAMPER is a creative thinking technique: Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse.',
    'Charrette': 'Charrette is a collaborative planning process involving multiple stakeholders in intensive workshops.',
    'Stepladder': 'Stepladder technique introduces team members one at a time to ensure all voices are heard before group discussion.'
}

# Business icon thinking styles
ICON_PERSPECTIVES = {
    'Jack Ma': 'emphasizing customer-first thinking, persistence through rejection, and building ecosystems',
    'Steve Jobs': 'focusing on design perfection, user experience, and thinking differently',
    'Peter Drucker': 'applying management science, asking what the customer values, and measuring what matters',
    'Mother Theresa': 'prioritizing compassion, serving the most vulnerable, and doing small things with great love',
    'Nikola Tesla': 'envisioning revolutionary innovation, pursuing wireless possibilities, and thinking decades ahead',
    'Sakichi Toyoda': 'applying the philosophy of continuous improvement (Kaizen) and asking why five times',
    'Estee Lauder': 'building personal relationships, believing in the product, and understanding customer aspirations',
    'Thomas Edision': 'experimenting persistently, learning from failure, and making innovation practical',
    'Henry Ford': 'standardizing processes, making products accessible, and empowering workers',
    'Andrew Carnegie': 'building strategic partnerships, vertical integration, and philanthropic legacy',
    'Sam Walton': 'obsessing over customer savings, learning from competition, and empowering associates',
    'Charles Schwab': 'democratizing access, reducing costs, and putting investor interests first',
    'Bill Gates': 'scaling technology for mass impact, strategic partnerships, and data-driven decisions',
    'Warren Buffett': 'seeking long-term value, understanding competitive moats, and staying within competence',
    'Indra Nooyi': 'balancing performance with purpose, thinking long-term, and strategic portfolio management',
    'Grace Hopper': 'making technology accessible, challenging the status quo, and asking forgiveness not permission',
    'Martin Luther King': 'appealing to moral principles, building coalitions, and envisioning a better future'
}


@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/app')
def application():
    """Main application page"""
    return render_template('app.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate brainstorming output using Gemini AI"""
    try:
        # Check if API is configured
        if not model:
            return jsonify({
                'success': False,
                'error': 'Gemini API is not configured. Please set GEMINI_API_KEY environment variable.'
            }), 500

        # Get form data
        data = request.json
        technique = data.get('technique')
        business_area = data.get('business_area')
        icon = data.get('icon')
        issue = data.get('issue')
        assumptions = data.get('assumptions')

        # Validate required fields
        if not technique or not issue:
            return jsonify({
                'success': False,
                'error': 'Technique and Issue are required fields.'
            }), 400

        # Build the prompt
        prompt = build_prompt(technique, business_area, icon, issue, assumptions)

        # Generate response from Gemini
        #response = model.generate_content(prompt)
        response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        #system_instruction=system_instruction,
                        # *** THE FIX: Force the model to generate valid JSON ***
                        #response_mime_type="application/json", 
                    )
        )
        
        # Extract the text from response
        output_text = response.text

        return jsonify({
            'success': True,
            'output': output_text
        })

    except Exception as e:
        print(f"Error in generate endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred while generating content: {str(e)}'
        }), 500


def build_prompt(technique, business_area, icon, issue, assumptions):
    """
    Build a comprehensive prompt for Gemini based on user inputs
    """
    # Start with system context
    prompt_parts = [
        "You are an expert business strategist and brainstorming facilitator.",
        f"Apply the {technique} brainstorming technique to analyze the following business challenge.",
        ""
    ]

    # Add technique context
    if technique in TECHNIQUE_CONTEXTS:
        prompt_parts.append(f"Technique Context: {TECHNIQUE_CONTEXTS[technique]}")
        prompt_parts.append("")

    # Add business area context
    if business_area:
        prompt_parts.append(f"Business Context: Focus on the {business_area} industry/sector.")
        prompt_parts.append("")

    # Add icon perspective
    if icon and icon in ICON_PERSPECTIVES:
        prompt_parts.append(f"Perspective: Approach this challenge as {icon} would, {ICON_PERSPECTIVES[icon]}.")
        prompt_parts.append("")

    # Add the main issue
    prompt_parts.append("Challenge/Issue:")
    prompt_parts.append(issue)
    prompt_parts.append("")

    # Add assumptions if provided
    if assumptions and assumptions.strip():
        prompt_parts.append("Assumptions and Constraints:")
        prompt_parts.append(assumptions)
        prompt_parts.append("")

    # Add instructions for output format
    prompt_parts.extend([
        "Please provide a comprehensive analysis using the specified technique. Structure your response in markdown format with:",
        "1. A brief summary of the challenge",
        "2. Application of the brainstorming technique with detailed analysis",
        "3. Key insights and recommendations",
        "4. Action items or next steps",
        "",
        "Use headers, bullet points, and formatting to make the output clear and actionable."
    ])

    return "\n".join(prompt_parts)


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Run the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
