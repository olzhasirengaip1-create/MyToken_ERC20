"""Загрузка настроек из .env."""
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL", "").strip()
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "").strip()
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "").strip()
ABI_PATH = os.getenv("ABI_PATH", "contract_abi.json").strip()