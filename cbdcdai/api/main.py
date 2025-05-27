"""
CBDCDAI API

FastAPI application providing REST API endpoints for CBDC simulation,
risk analytics, and regulatory compliance monitoring.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn

from ..simulation.cbdc_simulator import CBDCSimulator, CBDCParameters, EconomicIndicators
from ..risk.risk_analytics import RiskAnalytics, RiskMetrics
from ..compliance.regulatory_compliance import (
    RegulatoryCompliance,
    ComplianceMetrics,
    Jurisdiction,
    ComplianceRequirement
)

app = FastAPI(
    title="CBDCDAI API",
    description="Central Bank Digital Currency & Digital Assets Infrastructure API",
    version="1.0.0"
)

# Initialize core components
simulator = CBDCSimulator(
    CBDCParameters(
        interest_rate=0.02,
        reserve_requirement=0.1,
        transaction_limit=1000000,
        holding_limit=10000000,
        privacy_level=0.7,
        cross_border_enabled=True
    )
)

risk_engine = RiskAnalytics()
compliance_engine = RegulatoryCompliance()

# API Models
class SimulationRequest(BaseModel):
    policy_rate_change: float
    simulation_periods: int = 12

class CrossBorderRequest(BaseModel):
    amount: float
    source_currency: str
    target_currency: str
    exchange_rate: float

class RiskAssessmentRequest(BaseModel):
    returns: List[float]
    trading_metrics: Dict
    operational_metrics: Dict
    systemic_metrics: Dict

class ComplianceRequest(BaseModel):
    reserve_data: Dict
    transaction_data: Dict
    kyc_data: Dict
    aml_data: Dict

# API Routes
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "CBDCDAI API",
        "version": "1.0.0",
        "description": "Central Bank Digital Currency & Digital Assets Infrastructure API"
    }

@app.post("/simulation/monetary-transmission")
async def simulate_monetary_transmission(request: SimulationRequest):
    """Simulate monetary policy transmission"""
    try:
        results = simulator.simulate_monetary_transmission(
            request.policy_rate_change,
            request.simulation_periods
        )
        return results.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulation/cross-border")
async def simulate_cross_border(request: CrossBorderRequest):
    """Simulate cross-border payment"""
    try:
        results = simulator.simulate_cross_border_payment(
            request.amount,
            request.source_currency,
            request.target_currency,
            request.exchange_rate
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/simulation/financial-stability")
async def simulate_financial_stability(request: SimulationRequest):
    """Simulate financial stability impacts"""
    try:
        results = simulator.simulate_financial_stability(
            request.simulation_periods
        )
        return results.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/risk/assessment")
async def assess_risk(request: RiskAssessmentRequest):
    """Generate comprehensive risk assessment"""
    try:
        results = risk_engine.generate_risk_report(
            request.returns,
            request.trading_metrics,
            request.operational_metrics,
            request.systemic_metrics
        )
        return results.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/compliance/assessment")
async def assess_compliance(request: ComplianceRequest):
    """Generate compliance assessment"""
    try:
        results = compliance_engine.generate_compliance_report(
            request.reserve_data,
            request.transaction_data,
            request.kyc_data,
            request.aml_data
        )
        return results.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/compliance/jurisdictions")
async def get_jurisdictions():
    """Get supported jurisdictions"""
    return [jurisdiction.value for jurisdiction in Jurisdiction]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 