import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Firebase configuration
db = None
USE_MOCK = False

# Path to the service account key JSON file
cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')

if os.path.exists(cred_path):
    try:
        logger.info(f"Initializing Firebase Admin SDK using credentials from: {cred_path}")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        logger.info("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
        USE_MOCK = True
else:
    logger.warning(f"Firebase credentials file not found at {cred_path}. Falling back to Mock local database.")
    USE_MOCK = True

def get_db():
    """
    Returns the database client (Firestore or Mock).
    """
    global db, USE_MOCK
    if USE_MOCK:
        import firebase_mock
        return firebase_mock.get_mock_db()
    return db
