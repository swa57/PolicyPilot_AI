import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_response(prompt, context=""):
    """Get response from Google Gemini AI"""
    try:
        import google.generativeai as genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            return get_fallback_response(prompt)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        system_context = """You are PolicyPilot AI, an expert insurance claim verification and fraud detection assistant. 
        You help insurance agents and administrators:
        - Analyze insurance claims for fraud indicators
        - Explain suspicious patterns in claims
        - Summarize insurance documents
        - Answer questions about insurance policies and procedures
        - Provide risk assessments and recommendations
        
        Always be professional, precise, and helpful. Format responses clearly."""

        full_prompt = f"{system_context}\n\n{context}\n\nUser Question: {prompt}"

        response = model.generate_content(full_prompt)
        return response.text

    except ImportError:
        return "❌ google-generativeai not installed. Run: pip install google-generativeai"
    except Exception as e:
        return get_fallback_response(prompt, error=str(e))

def get_fallback_response(prompt, error=None):
    """Provide intelligent fallback responses without API"""
    prompt_lower = prompt.lower()

    responses = {
        "suspicious": """🔍 **Claim Suspicion Analysis:**

A claim is considered suspicious when it shows:
1. **High Fraud Score** (>40%) - ML model detected anomalies
2. **Unusual Amount** - Far exceeds historical averages for similar claims
3. **Duplicate Patterns** - Similar claims filed previously
4. **Suspicious Keywords** - Document contains red-flag terms
5. **Quick Filing** - Claim filed within days of policy start

**Recommended Actions:**
- Request additional documentation
- Verify hospital/provider authenticity
- Cross-check with police reports if accident involved
- Contact customer for clarification""",

        "fraud": """🚨 **Fraud Detection Explanation:**

Our AI model uses Random Forest Classifier trained on key indicators:

**High-Risk Indicators:**
• Fraud Score > 70% → FRAUDULENT
• Multiple duplicate claims
• Policy expired at claim time
• Claim amount 10x+ above average
• Suspicious terms in documents

**Medium-Risk Indicators:**
• Fraud Score 40-70% → SUSPICIOUS
• 3+ previous claims
• Claims filed very quickly
• Missing key documents

**Investigation Steps:**
1. Freeze claim processing
2. Request original bills
3. Contact hospital directly
4. File investigation report""",

        "summarize": """📄 **Document Summary Guidelines:**

When summarizing an insurance document, look for:

**Key Information:**
- Policy holder name and ID
- Coverage type and limits
- Premium amount and payment history
- Claim history (if any)
- Exclusions and special conditions

**Verification Points:**
- Document authenticity markers
- Matching information with claim form
- Medical necessity documentation
- Provider credentials""",

        "indicator": """⚠️ **Fraud Indicators Explained:**

**Financial Indicators:**
• Inflated claim amounts
• Round-number billing
• Charges without itemization

**Behavioral Indicators:**
• Pressure to settle quickly
• Reluctance to provide documents
• Changing story/timeline

**Document Indicators:**
• Altered/forged documents
• Missing signatures
• Inconsistent dates

**Pattern Indicators:**
• Repeated claims for same injury
• Claims after policy cancellation""",

        "approve": """✅ **Claim Approval Process:**

**For Genuine Claims (Score < 40%):**
1. All documents verified
2. No duplicate found
3. Hospital/provider verified
4. Amount within reasonable range
5. → APPROVE and process payment

**Standard Processing Timeline:**
- Initial review: 24-48 hours
- Document verification: 3-5 days
- Payment processing: 7-10 days""",
    }

    for key, response in responses.items():
        if key in prompt_lower:
            return response

    base_response = """🤖 **PolicyPilot AI Assistant**

I'm here to help with insurance claim analysis and fraud detection!

**I can help you with:**
- 🔍 Explain why a claim is suspicious
- 📄 Summarize insurance documents
- ⚠️ Identify fraud indicators
- ✅ Guide claim approval process
- 📊 Interpret risk scores

**Try asking:**
- "Why is this claim suspicious?"
- "What fraud indicators are present?"
- "How to verify a medical claim?"
- "Explain the fraud score"

💡 *To enable full AI responses, add your Gemini API key to the .env file.*"""

    if error:
        base_response += f"\n\n⚠️ API Error: {error}"

    return base_response

def get_claim_analysis_prompt(claim_data, fraud_result, indicators):
    """Generate analysis prompt for a specific claim"""
    return f"""Analyze this insurance claim for fraud:

Claim Details:
- Customer: {claim_data.get('customer_name', 'N/A')}
- Amount: ₹{claim_data.get('claim_amount', 0):,}
- Hospital: {claim_data.get('hospital_name', 'N/A')}
- Description: {claim_data.get('claim_description', 'N/A')}

AI Analysis Results:
- Fraud Probability: {fraud_result.get('fraud_probability', 0):.1f}%
- Risk Level: {fraud_result.get('risk_level', 'Unknown')}
- Prediction: {fraud_result.get('risk_label', 'N/A')}

Suspicious Indicators Found:
{chr(10).join(indicators)}

Please provide:
1. Detailed explanation of why this claim is or isn't suspicious
2. Specific risk factors identified
3. Recommended next steps for the insurance agent
4. Probability assessment explanation"""
