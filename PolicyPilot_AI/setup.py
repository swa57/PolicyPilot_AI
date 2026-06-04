#!/usr/bin/env python3
"""
PolicyPilot AI - Setup Script
Run this after extracting the ZIP to initialize the project.
"""

import os
import sys
import subprocess

def run_cmd(cmd, description):
    print(f"\n{'='*50}")
    print(f"⚙️  {description}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode == 0

def main():
    print("""
╔══════════════════════════════════════════════════╗
║       PolicyPilot AI - Setup Wizard             ║
║    Insurance Fraud Detection System              ║
╚══════════════════════════════════════════════════╝
    """)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Create directories
    dirs = ["uploads", "reports", "models", "dataset"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Directories created")

    # Install requirements
    success = run_cmd(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages..."
    )
    if not success:
        print("⚠️  Some packages may have failed. Continue anyway.")

    # Train ML model
    run_cmd(
        f"{sys.executable} models/train_model.py",
        "Training ML Fraud Detection Model..."
    )

    print("""
╔══════════════════════════════════════════════════╗
║            ✅ SETUP COMPLETE!                    ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  🚀 Run the app:                                 ║
║     streamlit run app.py                         ║
║                                                  ║
║  🔑 Login Credentials:                           ║
║     Admin : admin / admin123                     ║
║     Agent : agent1 / agent123                    ║
║                                                  ║
║  🤖 Optional - Add Gemini API Key:               ║
║     Edit .env file with your key                 ║
║     Get key: aistudio.google.com                 ║
║                                                  ║
╚══════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
