"""
Test Cases for Advanced Modules

Comprehensive test suite for advanced CBDCDAI modules, including:
- Economic models
- Risk models
- Compliance monitoring
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from cbdcdai.simulation.economic_models import EconomicModels, EconomicParameters
from cbdcdai.risk.advanced_risk_models import AdvancedRiskModels, NetworkMetrics, LiquidityMetrics
from cbdcdai.compliance.advanced_compliance import (
    AdvancedCompliance,
    ComplianceRequirement,
    ComplianceMetrics,
    RegulatoryFramework
)

# Test Economic Models
class TestEconomicModels:
    @pytest.fixture
    def economic_models(self):
        params = EconomicParameters(
            natural_rate=0.02,
            inflation_target=0.02,
            output_gap_weight=0.5,
            inflation_weight=1.5,
            money_velocity=1.5,
            fiscal_multiplier=1.0
        )
        return EconomicModels(params)
    
    def test_taylor_rule(self, economic_models):
        # Test Taylor Rule calculation
        interest_rate = economic_models.taylor_rule(
            inflation_rate=0.03,
            output_gap=0.01
        )
        assert isinstance(interest_rate, float)
        assert interest_rate > 0
    
    def test_phillips_curve(self, economic_models):
        # Test Phillips Curve calculation
        inflation = economic_models.phillips_curve(
            unemployment_rate=0.05,
            expected_inflation=0.02
        )
        assert isinstance(inflation, float)
    
    def test_is_lm_model(self, economic_models):
        # Test IS-LM model calculation
        output, interest = economic_models.is_lm_model(
            interest_rate=0.02,
            government_spending=1000,
            money_supply=5000,
            cbdc_adoption=0.1
        )
        assert isinstance(output, float)
        assert isinstance(interest, float)
    
    def test_money_multiplier(self, economic_models):
        # Test money multiplier calculation
        multiplier = economic_models.money_multiplier(
            reserve_ratio=0.1,
            currency_ratio=0.2,
            cbdc_ratio=0.1
        )
        assert isinstance(multiplier, float)
        assert multiplier > 0

# Test Risk Models
class TestAdvancedRiskModels:
    @pytest.fixture
    def risk_models(self):
        return AdvancedRiskModels()
    
    def test_network_risk(self, risk_models):
        # Test network risk calculation
        adjacency_matrix = np.array([
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0]
        ])
        metrics = risk_models.calculate_network_risk(adjacency_matrix)
        assert isinstance(metrics, NetworkMetrics)
        assert metrics.node_count == 4
        assert metrics.edge_count == 5
    
    def test_liquidity_risk(self, risk_models):
        # Test liquidity risk calculation
        trading_data = {
            'volume': 1000000,
            'market_cap': 10000000,
            'spread': 0.001,
            'depth': 500000
        }
        metrics = risk_models.calculate_liquidity_risk(trading_data)
        assert isinstance(metrics, LiquidityMetrics)
        assert metrics.trading_volume == 1000000
    
    def test_operational_risk(self, risk_models):
        # Test operational risk assessment
        system_metrics = {
            'uptime': 0.999,
            'response_time': 0.1,
            'target_response_time': 0.2,
            'security_incidents': 2,
            'total_incidents': 100
        }
        risk_score = risk_models.assess_operational_risk(system_metrics)
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 1
    
    def test_systemic_risk(self, risk_models):
        # Test systemic risk assessment
        network_metrics = NetworkMetrics(
            node_count=4,
            edge_count=5,
            average_degree=2.5,
            clustering_coefficient=0.5,
            centralization=0.3
        )
        liquidity_metrics = LiquidityMetrics(
            trading_volume=1000000,
            bid_ask_spread=0.001,
            market_depth=500000,
            turnover_ratio=0.1,
            liquidity_ratio=0.8
        )
        risk_score = risk_models.assess_systemic_risk(
            network_metrics,
            liquidity_metrics,
            operational_risk=0.2
        )
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 1

# Test Compliance Monitoring
class TestAdvancedCompliance:
    @pytest.fixture
    def compliance_engine(self):
        return AdvancedCompliance()
    
    def test_mica_compliance(self, compliance_engine):
        # Test MiCA compliance checking
        metrics = compliance_engine.check_mica_compliance(
            reserve_data={'ratio': 1.0},
            transaction_data={'amount': 500000}
        )
        assert isinstance(metrics, ComplianceMetrics)
        assert metrics.framework == RegulatoryFramework.MICA
    
    def test_genius_compliance(self, compliance_engine):
        # Test GENIUS Act compliance checking
        metrics = compliance_engine.check_genius_compliance(
            stablecoin_data={'reserve_ratio': 1.0},
            kyc_data={'completion_rate': 0.98}
        )
        assert isinstance(metrics, ComplianceMetrics)
        assert metrics.framework == RegulatoryFramework.GENIUS
    
    def test_compliance_report(self, compliance_engine):
        # Test compliance report generation
        metrics = [
            ComplianceMetrics(
                framework=RegulatoryFramework.MICA,
                requirement_id="MICA_001",
                compliance_score=0.9,
                last_check=datetime.now(),
                next_check=datetime.now() + timedelta(days=1),
                violations=[],
                corrective_actions=[],
                status="Compliant"
            )
        ]
        report = compliance_engine.generate_compliance_report(metrics)
        assert isinstance(report, pd.DataFrame)
        assert len(report) == 1
    
    def test_regulatory_changes(self, compliance_engine):
        # Test regulatory change monitoring
        current_requirements = [
            ComplianceRequirement(
                framework=RegulatoryFramework.MICA,
                requirement_id="MICA_001",
                description="Test requirement",
                threshold=1.0,
                monitoring_frequency="daily",
                reporting_frequency="monthly",
                effective_date=datetime.now(),
                jurisdiction="EU",
                category="Test"
            )
        ]
        new_requirements = [
            ComplianceRequirement(
                framework=RegulatoryFramework.MICA,
                requirement_id="MICA_001",
                description="Modified requirement",
                threshold=1.1,
                monitoring_frequency="daily",
                reporting_frequency="monthly",
                effective_date=datetime.now(),
                jurisdiction="EU",
                category="Test"
            )
        ]
        changes = compliance_engine.monitor_regulatory_changes(
            current_requirements,
            new_requirements
        )
        assert isinstance(changes, list)
        assert len(changes) > 0
    
    def test_risk_score(self, compliance_engine):
        # Test compliance risk score calculation
        metrics = [
            ComplianceMetrics(
                framework=RegulatoryFramework.MICA,
                requirement_id="MICA_001",
                compliance_score=0.9,
                last_check=datetime.now(),
                next_check=datetime.now() + timedelta(days=1),
                violations=[],
                corrective_actions=[],
                status="Compliant"
            )
        ]
        risk_score = compliance_engine.calculate_risk_score(metrics)
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 1 