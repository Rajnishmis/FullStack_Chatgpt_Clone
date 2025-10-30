# from pydantic_settings import BaseSettings, SettingsConfigDict
# import os

# # COPY THIS OUTPUT AND PASTE IT INTO YOUR .env FILE!


# class AppSettings(BaseSettings):
#     database_url: str
#     jwt_secret: str
#     openai_api_key: str

#     # Configure the Dictionary !!!!
#     model_config = SettingsConfigDict(
#         # The file to read env variables from
#         env_file=(".env"),

#         # Specifies if the .env file is manadatory
#         env_ignore_empty=True
#     )


# try:
#     CONFIG = AppSettings()
#     print("--- Configuration Loaded Successfully (V2) ---")
#     print(f"Database URL: {CONFIG.database_url}")
#     # print(f"JWT Secret: {CONFIG.jwt_secret}") # Avoid printing secrets
#     LOAD_SUCCESS = True
# except Exception as e:
#     print(f"Error loading settings: {e}")
#     LOAD_SUCCESS = False


# # 3. Verification Section (Runs only if load was successful)
# if LOAD_SUCCESS:
#     print("\n✅ CONFIGURATION LOAD SUCCESSFUL\n" + "="*35)

#     # --- Check 1: JWT_SECRET (Required Variable) ---
#     print(f"[Check 1/3] JWT Secret Length: {len(CONFIG.jwt_secret)}")
#     # Assert that the secret is at least 32 characters long (a good security practice)
#     assert len(
#         CONFIG.jwt_secret) >= 32, "SECURITY WARNING: JWT_SECRET is too short."

#     # --- Check 2: LOG_LEVEL (Overridden Default) ---
#     # This assumes your .env file set LOG_LEVEL="DEBUG"
#     expected_log_level = os.environ.get("LOG_LEVEL") or "DEBUG"

#     # --- Check 3: DATABASE_URL (Respects Default if Missing) ---
#     # To test the default, temporarily comment out DATABASE_URL in your .env file.
#     if "DATABASE_URL" not in os.environ and not os.path.exists(".env"):
#         print(f"[Check 3/3] DB URL Default: {CONFIG.database_url}")
#         assert CONFIG.database_url == "sqlite:///./test.db", "Default DB URL was not used."
#     else:
#         print(f"[Check 3/3] DB URL Loaded: {CONFIG.database_url[:25]}...")
#         assert "postgresql" in CONFIG.database_url or "sqlite" in CONFIG.database_url, "DB URL format looks wrong."

#     print("="*35 + "\n✅ ALL CONFIGURATION CHECKS PASSED.")

# # You can now import CONFIG from this file in other modules.


import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
