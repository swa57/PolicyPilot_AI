# 🛡️ PolicyPilot AI – Insurance Claim Verification & Fraud Analysis System

> An AI-powered insurance fraud detection platform built with Streamlit, Machine Learning, and Google Gemini AI.

---

## 📸 Features

| Feature | Description |
|---|---|
| 🔐 Login System | Admin & Agent roles with session management |
| 📊 Dashboard | Real-time KPIs, charts, fraud analytics |
| 📝 Claim Submission | Form with document upload (PDF/Image) |
| 🔍 OCR Analysis | Extract text from PDFs and images |
| 🤖 AI Fraud Detection | Random Forest ML model |
| 📄 Risk Reports | Auto-generated TXT/PDF reports |
| 💬 Gemini Chatbot | AI-powered insurance assistant |
| 🛠️ Admin Panel | Approve/reject claims, user management |
| 📈 Visual Analytics | Plotly charts and fraud trend analysis |

---

## 🚀 Quick Setup

### Step 1: Extract the ZIP
```bash
unzip PolicyPilot_AI.zip
cd PolicyPilot_AI
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Tesseract OCR (for image text extraction)
- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Mac:** `brew install tesseract`
- **Linux/Ubuntu:** `sudo apt install tesseract-ocr`

### Step 5: Configure Gemini API Key (Optional)
Edit the `.env` file:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
Get your free API key from: https://aistudio.google.com/app/apikey

### Step 6: Train the ML Model
```bash
cd PolicyPilot_AI
python models/train_model.py
```

### Step 7: Run the Application
```bash
streamlit run app.py
```

Open browser: **http://localhost:8501**

---

## 🔑 Login Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Agent | `agent1` | `agent123` |
| Agent | `agent2` | `pass456` |

---

## 📁 Project Structure

```
PolicyPilot_AI/
│
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── claims.csv                # Claims database
├── users.csv                 # User credentials
├── .env                      # API keys configuration
│
├── uploads/                  # Uploaded claim documents
├── reports/                  # Generated risk reports
│
├── models/
│   ├── train_model.py        # ML model training script
│   ├── fraud_model.pkl       # Trained model (auto-generated)
│   └── scaler.pkl            # Feature scaler (auto-generated)
│
├── dataset/
│   └── insurance_claims.csv  # Training dataset
│
├── pages/
│   ├── dashboard.py          # Dashboard with charts
│   ├── submit_claim.py       # Claim submission form
│   ├── fraud_detection.py    # AI fraud analysis
│   ├── reports.py            # Reports center
│   ├── chatbot.py            # Gemini AI chatbot
│   └── admin_panel.py        # Admin management
│
└── utils/
    ├── auth.py               # Authentication system
    ├── ocr_utils.py          # OCR text extraction
    ├── fraud_utils.py        # Fraud detection utilities
    ├── report_generator.py   # Report generation
    └── gemini_chat.py        # Gemini AI integration
```

---

## 🤖 How the AI Works

### Machine Learning (Fraud Detection)
- **Algorithm:** Random Forest Classifier
- **Features used:**
  - `claim_amount` - Size of the claim
  - `claim_frequency` - How often this customer claims
  - `duplicate_claim` - Similar claim exists?
  - `suspicious_keywords` - Red-flag terms in description
  - `policy_expired` - Was policy active?
  - `days_since_policy` - Policy age at claim time
  - `num_previous_claims` - Historical claim count
  - `amount_vs_avg_ratio` - Amount vs. average
  - `incident_to_claim_days` - Speed of filing

- **Output:**
  - 🟢 Genuine Claim (0–40%)
  - 🟡 Suspicious Claim (40–70%)
  - 🔴 Fraudulent Claim (70–100%)

### OCR (Document Analysis)
- PDF: PyPDF2 text extraction
- Images: pytesseract (Tesseract OCR engine)
- Detects: missing fields, suspicious keywords, document completeness

### Gemini AI Chatbot
- Uses Google Gemini 1.5 Flash model
- Explains fraud indicators
- Summarizes claim documents
- Answers insurance questions
- Falls back to intelligent responses if API key not set

---

## 🛠️ Troubleshooting

**Q: Model not found error?**
```bash
python models/train_model.py
```

**Q: pytesseract error?**
- Install Tesseract OCR engine (see Step 4 above)
- On Windows, set path: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

**Q: Gemini API not working?**
- Add your API key to `.env` file
- The chatbot works without API key using built-in responses

**Q: Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

---

## 📊 Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit + Custom CSS |
| ML Model | Random Forest (scikit-learn) |
| OCR | pytesseract + PyPDF2 |
| AI Chatbot | Google Gemini 1.5 Flash |
| Charts | Plotly Express |
| Storage | CSV files |
| Reports | TXT + ReportLab PDF |

---

## 📝 Interview Talking Points

1. **Streamlit** - Rapid UI development for data science apps
2. **Random Forest** - Ensemble ML for fraud classification
3. **OCR** - Automated document verification with Tesseract
4. **Gemini AI** - LLM integration for intelligent explanations
5. **CSV Storage** - Lightweight, no-database architecture
6. **Session Management** - Stateful authentication with Streamlit

---

*Built with ❤️ for Insurance AI Innovation*
