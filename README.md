activate the venv using: source venv/bin/activate

# 🤖 Hybrid AI Stock Analyst

This project is an AI-driven decision-support system designed to construct a comprehensive, evidence-based investment thesis for individual stocks. It moves beyond simple price prediction by synthesizing four distinct pillars of analysis—Fundamental, Technical, Macroeconomic, and Narrative (Sentiment)—into a single, coherent, and explainable forecast.

---

## 🚀 Getting Started (User Guide)

Follow these instructions to set up and run the interactive analysis dashboard on your local machine.

### 1. Prerequisites

- Python 3.9+ installed on your system.
- Access to a command line or terminal.

### 2. Setup

First, clone the project repository to your local machine (or simply use the project folder you already have).

Navigate to the project's root directory in your terminal:
```bash
cd path/to/your/ai_stock_analyst
```

Create and activate a Python virtual environment. This keeps the project's dependencies isolated.
```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

Install all the necessary Python libraries for both the backend and frontend with the following commands:
```bash
# Install backend requirements
pip install -r backend/requirements.txt

# Install frontend requirements
pip install -r frontend/requirements.txt
```

### 4. Run the Application

Launch the Streamlit dashboard with this command:
```bash
streamlit run frontend/app.py
```

Your default web browser will automatically open a new tab with the application running. You can now enter a stock ticker and begin your analysis!

---

## 🛠️ Project Architecture (Developer Info)

*(This section will be filled in later with details about the backend pipelines, model training, and overall system design.)*