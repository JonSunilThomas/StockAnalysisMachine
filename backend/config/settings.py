# backend/config/settings.py

from dotenv import load_dotenv
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This makes sure your paths work on any operating system.
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = BASE_DIR / '.env'

# Load the .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

# --- API Keys ---
FRED_API_KEY = os.getenv("FRED_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# --- Data File Paths ---
# You can define common data paths here to keep your project organized.
RAW_DATA_DIR = BASE_DIR / "data/raw/"
PROCESSED_DATA_DIR = BASE_DIR / "data/processed/"


# --- Sanity Check ---
# A quick check to ensure keys are loaded. The script will raise an error if a key is missing.
if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY is not set in the .env file.")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY is not set in the .env file.")