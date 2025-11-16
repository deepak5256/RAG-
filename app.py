from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure your Gemini API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not found in environment variables")
    print("Please create a .env file with your API key")

# Comprehensive Company Knowledge Base
COMPANY_KNOWLEDGE_BASE = {
    # Company Basic Information
    "company overview": {
        "content": "TechCorp Inc. is a leading SaaS company founded in 2018 specializing in AI-powered business intelligence solutions. We help enterprises transform raw data into actionable insights through our innovative platform.",
        "source": "Company Overview Document",
        "last_updated": "2024-03-01"
    },
    
    "founders": {
        "content": "Co-founded by Sarah Chen (CEO) and Mark Rodriguez (CTO). Sarah previously led product at DataTech Solutions, while Mark was the lead AI researcher at Stanford University. They started TechCorp with a vision to democratize AI for businesses of all sizes.",
        "source": "Company History & Founders",
        "last_updated": "2024-01-15"
    },
    
    "mission vision": {
        "content": "Mission: To empower every organization with intelligent decision-making tools. Vision: To become the world's most trusted AI-powered business intelligence platform by 2030.",
        "source": "Company Mission & Vision",
        "last_updated": "2024-01-10"
    },
    
    "company values": {
        "content": "Our core values: 1) Innovation First, 2) Customer Obsession, 3) Transparency Always, 4) Excellence in Execution, 5) Collaborative Growth. These values guide every decision we make.",
        "source": "Company Values Handbook",
        "last_updated": "2024-02-01"
    },
    
    "what we do": {
        "content": "We provide an AI-powered business intelligence platform that includes: Data Analytics, Predictive Modeling, Automated Reporting, Real-time Dashboards, and Custom AI Solutions. Our platform integrates with 50+ data sources including Salesforce, Google Analytics, and SQL databases.",
        "source": "Product & Services Overview",
        "last_updated": "2024-03-10"
    },
    
    "company size": {
        "content": "Currently we have 250 employees globally. Headquarters: San Francisco (150 employees), Additional offices: New York (50), London (30), Singapore (20). We're planning to expand to Berlin in Q3 2024.",
        "source": "HR Organizational Chart",
        "last_updated": "2024-03-15"
    },
    
    "key achievements": {
        "content": "2023: Reached 10,000 customers globally, 2022: Series B funding $50M, 2021: Named 'Most Innovative AI Company' by TechCrunch, 2020: Reached profitability, 2019: Launched flagship product 'InsightAI', 2018: Company founded with seed funding of $2M",
        "source": "Company Milestones",
        "last_updated": "2024-01-20"
    },
    
    "company culture": {
        "content": "We foster a culture of continuous learning with weekly tech talks, monthly hackathons, and annual learning stipend of $3000 per employee. Our office features standing desks, meditation rooms, and free healthy snacks. We have 15 employee resource groups.",
        "source": "Culture Code Document",
        "last_updated": "2024-02-28"
    },

    # HR Policies
    "vacation policy": {
        "content": "As of 2024, employees get 20 vacation days per year. Unused days can be rolled over up to 5 days. New policy: Starting Q2 2024, we're implementing unlimited mental health days with manager approval.",
        "source": "HR Policy Document v3.2",
        "last_updated": "2024-03-15"
    },
    
    "remote work policy": {
        "content": "Current hybrid schedule: 3 days in office (Tue-Thu), 2 days remote. Office hours: 9 AM - 5 PM. New requirement: All employees must attend monthly in-person team building on first Friday.",
        "source": "Remote Work Guidelines 2024",
        "last_updated": "2024-02-28"
    },
    
    "health insurance": {
        "content": "We offer Blue Cross Blue Shield PPO. Deductible: $500 individual, $1500 family. Dental and vision included. New for 2024: Added mental health coverage with $20 copay.",
        "source": "Benefits Package 2024",
        "last_updated": "2024-01-10"
    },
    
    # Product Information
    "product pricing": {
        "content": "Starter Plan: $49/month (up to 5 users), Pro Plan: $99/month (up to 20 users), Enterprise: $299/month (unlimited users). Current promotion: 20% off annual billing until March 31, 2024.",
        "source": "Product Pricing Sheet Q1 2024",
        "last_updated": "2024-03-01"
    },
    
    "new features": {
        "content": "Recently launched: AI-powered analytics dashboard (March 2024), Advanced reporting suite (February 2024), Mobile app redesign (January 2024). Coming soon: Integration with Slack (April 2024), Advanced predictive modeling (May 2024).",
        "source": "Product Roadmap",
        "last_updated": "2024-03-20"
    },
    
    "product offerings": {
        "content": "Main products: 1) InsightAI (flagship BI platform), 2) PredictPro (advanced forecasting), 3) ReportRocket (automated reporting), 4) DataConnect (integration hub). All products include 24/7 support and weekly training sessions.",
        "source": "Product Catalog 2024",
        "last_updated": "2024-02-15"
    },
    
    # Company Procedures
    "expense reimbursement": {
        "content": "Submit expenses within 30 days via Expensify. Limits: Meals $75, Travel $300/night. New policy: Uber/Lyft reimbursed for work after 7 PM. Required receipts for all expenses over $25.",
        "source": "Finance Policy Handbook",
        "last_updated": "2024-02-15"
    },
    
    "performance reviews": {
        "content": "Bi-annual reviews in June and December. New 360-degree feedback system implemented in 2024. Ratings: Exceeds, Meets, Needs Improvement. Calibration sessions occur first week of review month.",
        "source": "Performance Management Guide",
        "last_updated": "2024-01-20"
    },
    
    # Internal Contacts
    "key contacts": {
        "content": "IT Support: help@company.com (responds within 2 hours), HR: hr@company.com, Facilities: facilities@company.com. New hires: Contact Sarah Johnson in HR for onboarding. Emergency contact: security@company.com. Founders: Sarah Chen (sarah@company.com), Mark Rodriguez (mark@company.com)",
        "source": "Internal Contacts Directory",
        "last_updated": "2024-03-10"
    },
    
    "company events": {
        "content": "Q2 2024 Events: All-hands meeting April 15, Summer party June 21, Team offsite May 10-11 in Lake Tahoe. New: Monthly 'Lunch and Learn' sessions starting April 2024. Annual company retreat: September 15-18 in Hawaii.",
        "source": "Company Events Calendar",
        "last_updated": "2024-03-18"
    },
    
    "departments": {
        "content": "Main departments: Engineering (80 employees), Product (30), Sales (60), Marketing (25), Customer Success (35), HR (10), Finance (10). Each department has monthly all-hands meetings and quarterly planning sessions.",
        "source": "Organizational Structure",
        "last_updated": "2024-02-20"
    },
    
    "career growth": {
        "content": "We offer: 1) $3000 annual learning budget, 2) Mentorship program with senior leaders, 3) Clear promotion tracks (Junior → Mid → Senior → Lead → Principal), 4) Quarterly career development conversations with managers, 5) Internal mobility program.",
        "source": "Career Development Framework",
        "last_updated": "2024-01-30"
    },
    
    "diversity inclusion": {
        "content": "Current diversity stats: 45% women in tech roles, 35% leadership from underrepresented groups. Initiatives: Unconscious bias training, Diverse hiring panels, 15 employee resource groups, Annual diversity report published transparently.",
        "source": "DEI Report 2024",
        "last_updated": "2024-02-10"
    }
}

def test_api_key():
    """Test if the API key is valid"""
    try:
        if not GEMINI_API_KEY:
            return False, "API key not found in environment variables"
        
        genai.configure(api_key=GEMINI_API_KEY)
        # Try gemini-2.0-flash-exp as it's the latest available model
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content("Say 'API test successful'")
            return True, "API key is valid - Using gemini-2.5-flash"
        except Exception as model_error:
            # Fallback to gemini-1.5-flash if 2.0 is not available
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content("Say 'API test successful'")
                return True, "API key is valid - Using gemini-1.5-flash (2.0 not available)"
            except Exception:
                return False, f"Model error: {str(model_error)}"
                
    except Exception as e:
        return False, f"API key error: {str(e)}"

def get_available_model():
    """Get the best available model"""
    try:
        # Try the latest model first
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Test if model is available
        test_response = model.generate_content("test")
        return 'gemini-2.5-flash'
    except Exception:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            test_response = model.generate_content("test")
            return 'gemini-1.5-flash'
        except Exception:
            return None

def retrieve_relevant_info(query):
    """
    Enhanced retrieval with comprehensive keyword mappings
    """
    query_lower = query.lower()
    relevant_info = []
    
    # Comprehensive keyword mappings
    keyword_mappings = {
        'company': ['company overview', 'about company', 'what is techcorp', 'who we are', 'company info'],
        'founders': ['founders', 'ceo', 'cto', 'sarah chen', 'mark rodriguez', 'leadership'],
        'mission': ['mission', 'vision', 'values', 'purpose', 'why we exist'],
        'products': ['what we do', 'products', 'services', 'offerings', 'platform'],
        'size': ['company size', 'employees', 'team size', 'how many people'],
        'achievements': ['achievements', 'milestones', 'awards', 'funding', 'success'],
        'culture': ['company culture', 'work environment', 'values', 'work life'],
        'vacation': ['vacation policy', 'time off', 'pto', 'holiday', 'days off'],
        'remote': ['remote work policy', 'wfh', 'work from home', 'hybrid', 'remote'],
        'insurance': ['health insurance', 'benefits', 'medical', 'dental', 'insurance'],
        'pricing': ['product pricing', 'cost', 'price', 'subscription', 'how much'],
        'features': ['new features', 'product updates', 'launch', 'roadmap', 'whats new'],
        'expense': ['expense reimbursement', 'expenses', 'reimbursement', 'expense'],
        'review': ['performance reviews', 'performance', 'feedback', 'review'],
        'contact': ['key contacts', 'who to contact', 'support', 'hr', 'contact'],
        'event': ['company events', 'meetings', 'party', 'all-hands', 'events'],
        'departments': ['departments', 'teams', 'engineering', 'sales', 'marketing'],
        'career': ['career growth', 'promotion', 'development', 'learning', 'growth'],
        'diversity': ['diversity', 'inclusion', 'dei', 'equity', 'representation']
    }
    
    # Find relevant documents based on keyword mappings
    matched_docs = set()
    for category, keywords in keyword_mappings.items():
        if any(keyword in query_lower for keyword in keywords):
            # Map to actual document names
            mapping = {
                'company': 'company overview',
                'founders': 'founders',
                'mission': 'mission vision',
                'products': 'what we do',
                'size': 'company size',
                'achievements': 'key achievements',
                'culture': 'company culture',
                'vacation': 'vacation policy',
                'remote': 'remote work policy',
                'insurance': 'health insurance',
                'pricing': 'product pricing',
                'features': 'new features',
                'expense': 'expense reimbursement',
                'review': 'performance reviews',
                'contact': 'key contacts',
                'event': 'company events',
                'departments': 'departments',
                'career': 'career growth',
                'diversity': 'diversity inclusion'
            }
            if category in mapping:
                matched_docs.add(mapping[category])
    
    # Also do direct matching
    for key in COMPANY_KNOWLEDGE_BASE.keys():
        if any(word in query_lower for word in key.split()):
            matched_docs.add(key)
    
    # Convert to list of info objects
    for doc in matched_docs:
        if doc in COMPANY_KNOWLEDGE_BASE:
            info = COMPANY_KNOWLEDGE_BASE[doc]
            relevant_info.append({
                "source": f"{info['source']} (Updated: {info['last_updated']})",
                "content": info['content'],
                "title": doc.replace('_', ' ').title()
            })
    
    return relevant_info

def format_context_for_prompt(retrieved_info):
    """Format the retrieved information for the Gemini prompt"""
    if not retrieved_info:
        return "No specific company documents found for this query."
    
    context_parts = ["RETRIEVED COMPANY KNOWLEDGE:"]
    
    for i, info in enumerate(retrieved_info, 1):
        context_parts.append(f"""
DOCUMENT {i}: {info['title']}
SOURCE: {info['source']}
CONTENT: {info['content']}
""")
    
    return "\n".join(context_parts)

def generate_rag_response(query, retrieved_info):
    """Generate response using Gemini with retrieved context"""
    try:
        if not GEMINI_API_KEY:
            return generate_fallback_response(query, retrieved_info)
            
        genai.configure(api_key=GEMINI_API_KEY)
        model_name = get_available_model()
        
        if not model_name:
            return generate_fallback_response(query, retrieved_info)
            
        model = genai.GenerativeModel(model_name)
        
        context = format_context_for_prompt(retrieved_info)
        
        prompt = f"""
You are a helpful assistant for TechCorp Inc. Use ONLY the retrieved company information below to answer the question. 
If the information isn't in the retrieved documents, say "This information is not available in our company knowledge base."

{context}

QUESTION: {query}

IMPORTANT INSTRUCTIONS:
1. Answer based ONLY on the retrieved company documents above
2. Be specific with numbers, dates, and policies mentioned
3. If information is missing, don't make up answers
4. Mention that your answer is based on company documents
5. Keep responses concise and helpful

ANSWER:
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error generating RAG response: {str(e)}"

def generate_direct_response(query):
    """Generate response without RAG for comparison"""
    try:
        if not GEMINI_API_KEY:
            return "Cannot generate direct response: API key not configured"
            
        genai.configure(api_key=GEMINI_API_KEY)
        model_name = get_available_model()
        
        if not model_name:
            return "Cannot generate direct response: No available model"
            
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
Answer the following question about a company using only your general knowledge.
Do not pretend to have specific information about company policies or details.

QUESTION: {query}

If you don't have specific information, be honest about what you don't know.
Provide a general answer based on common practices, but make it clear this is not company-specific. or just say that i dont have the information you need.

ANSWER:
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error generating direct response: {str(e)}"

def generate_fallback_response(query, retrieved_info):
    """Generate a fallback response when API fails"""
    if retrieved_info:
        response_parts = ["Based on our company knowledge base:\n\n"]
        for info in retrieved_info:
            response_parts.append(f"• {info['title']}: {info['content']}\n")
        return "".join(response_parts)
    else:
        return "I don't have specific information about this in our company knowledge base. Please check with HR or relevant department."

@app.route('/')
def index():
    # Test API key on homepage load
    api_valid, api_message = test_api_key()
    return render_template('index.html', api_valid=api_valid, api_message=api_message)

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        query = request.form.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter a question'})
        
        # Test API key first
        api_valid, api_message = test_api_key()
        if not api_valid:
            # Use fallback responses if API is invalid
            retrieved_info = retrieve_relevant_info(query)
            rag_response = generate_fallback_response(query, retrieved_info)
            direct_response = "Cannot generate direct response: " + api_message
            
            return render_template('result.html', 
                                 query=query,
                                 retrieved_info=retrieved_info,
                                 rag_response=rag_response,
                                 direct_response=direct_response,
                                 rag_advantage=len(retrieved_info) > 0,
                                 api_error=api_message)
        
        # Step 1: Retrieve relevant information
        retrieved_info = retrieve_relevant_info(query)
        
        # Step 2: Generate RAG response
        rag_response = generate_rag_response(query, retrieved_info)
        
        # Step 3: Generate direct response for comparison
        direct_response = generate_direct_response(query)
        
        # Determine which response is better
        rag_advantage = len(retrieved_info) > 0
        
        return render_template('result.html', 
                             query=query,
                             retrieved_info=retrieved_info,
                             rag_response=rag_response,
                             direct_response=direct_response,
                             rag_advantage=rag_advantage)
                             
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

@app.route('/test-api')
def test_api_route():
    """Route to test API key"""
    api_valid, api_message = test_api_key()
    return jsonify({
        'valid': api_valid,
        'message': api_message
    })

if __name__ == '__main__':
    # Test API key on startup
    print("Testing API key...")
    api_valid, api_message = test_api_key()
    if api_valid:
        print("✅ API key is valid! Starting server...")
    else:
        print("❌ API key error:", api_message)
        print("Please check your .env file and ensure GEMINI_API_KEY is set")
    
    app.run(debug=True, host='0.0.0.0', port=5000)