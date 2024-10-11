from rewards_backend.settings.base import firebase_config

from firebase_admin import credentials
import firebase_admin

cred = credentials.Certificate(firebase_config)
firebase_app = firebase_admin.initialize_app(cred)
