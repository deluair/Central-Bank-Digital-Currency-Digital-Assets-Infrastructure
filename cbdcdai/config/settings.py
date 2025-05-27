"""
Configuration Settings

This module manages configuration settings and environment variables for the CBDCDAI platform.
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CBDCDAI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Central Bank Digital Currency & Digital Assets Infrastructure"
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cbdcai.db")
    
    # Simulation Settings
    DEFAULT_SIMULATION_PERIODS: int = 12
    DEFAULT_INTEREST_RATE: float = 0.02
    DEFAULT_RESERVE_REQUIREMENT: float = 0.1
    DEFAULT_TRANSACTION_LIMIT: float = 1000000
    DEFAULT_HOLDING_LIMIT: float = 10000000
    
    # Risk Settings
    VAR_CONFIDENCE_LEVEL: float = 0.95
    DEFAULT_RISK_THRESHOLD: float = 0.7
    
    # Compliance Settings
    COMPLIANCE_REPORTING_FREQUENCY: str = "daily"
    KYC_THRESHOLD: float = 0.95
    AML_RISK_THRESHOLD: float = 0.7
    
    # Cross-border Settings
    CROSS_BORDER_ENABLED: bool = True
    DEFAULT_SETTLEMENT_TIME: int = 2  # minutes
    
    # Monitoring Settings
    MONITORING_INTERVAL: int = 60  # seconds
    ALERT_THRESHOLD: float = 0.8
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()

# Export settings
__all__ = ["settings"] 