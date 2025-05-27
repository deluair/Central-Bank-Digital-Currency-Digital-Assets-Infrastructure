"""
Advanced Compliance Monitoring

Enhanced regulatory compliance monitoring capabilities for CBDC operations,
including multi-jurisdictional compliance tracking, automated reporting,
and regulatory change management.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from enum import Enum

class RegulatoryFramework(str, Enum):
    """Supported regulatory frameworks"""
    MICA = "MICA"  # EU Markets in Crypto-Assets
    GENIUS = "GENIUS"  # US Stablecoin Regulation
    FSB = "FSB"  # Financial Stability Board
    BIS = "BIS"  # Bank for International Settlements
    FATF = "FATF"  # Financial Action Task Force

class ComplianceRequirement(BaseModel):
    """Detailed compliance requirement"""
    framework: RegulatoryFramework
    requirement_id: str
    description: str
    threshold: float
    monitoring_frequency: str
    reporting_frequency: str
    effective_date: datetime
    expiry_date: Optional[datetime]
    jurisdiction: str
    category: str

class ComplianceMetrics(BaseModel):
    """Detailed compliance metrics"""
    framework: RegulatoryFramework
    requirement_id: str
    compliance_score: float
    last_check: datetime
    next_check: datetime
    violations: List[str]
    corrective_actions: List[str]
    status: str

class AdvancedCompliance:
    """Advanced compliance monitoring engine"""
    
    def __init__(self):
        self.requirements = {}
        self.metrics = {}
        self.reporting_schedules = {}
        
    def add_requirement(self, requirement: ComplianceRequirement):
        """Add compliance requirement"""
        key = f"{requirement.framework}_{requirement.requirement_id}"
        self.requirements[key] = requirement
        
    def check_mica_compliance(self,
                            reserve_data: Dict,
                            transaction_data: Dict) -> ComplianceMetrics:
        """
        Check MiCA compliance
        
        Args:
            reserve_data: Reserve adequacy data
            transaction_data: Transaction data
            
        Returns:
            ComplianceMetrics object
        """
        violations = []
        corrective_actions = []
        
        # Check reserve requirements
        if reserve_data['ratio'] < 1.0:
            violations.append("Insufficient reserves")
            corrective_actions.append("Increase reserve holdings")
        
        # Check transaction limits
        if transaction_data['amount'] > 1000000:  # €1M limit
            violations.append("Transaction limit exceeded")
            corrective_actions.append("Implement transaction limits")
        
        # Calculate compliance score
        compliance_score = 1.0 - (len(violations) * 0.2)
        
        return ComplianceMetrics(
            framework=RegulatoryFramework.MICA,
            requirement_id="MICA_001",
            compliance_score=compliance_score,
            last_check=datetime.now(),
            next_check=datetime.now() + timedelta(days=1),
            violations=violations,
            corrective_actions=corrective_actions,
            status="Compliant" if compliance_score >= 0.8 else "Non-compliant"
        )
    
    def check_genius_compliance(self,
                              stablecoin_data: Dict,
                              kyc_data: Dict) -> ComplianceMetrics:
        """
        Check GENIUS Act compliance
        
        Args:
            stablecoin_data: Stablecoin data
            kyc_data: KYC data
            
        Returns:
            ComplianceMetrics object
        """
        violations = []
        corrective_actions = []
        
        # Check reserve requirements
        if stablecoin_data['reserve_ratio'] < 1.0:
            violations.append("Insufficient reserves")
            corrective_actions.append("Increase reserve holdings")
        
        # Check KYC requirements
        if kyc_data['completion_rate'] < 0.95:
            violations.append("Incomplete KYC")
            corrective_actions.append("Complete KYC for all users")
        
        # Calculate compliance score
        compliance_score = 1.0 - (len(violations) * 0.2)
        
        return ComplianceMetrics(
            framework=RegulatoryFramework.GENIUS,
            requirement_id="GENIUS_001",
            compliance_score=compliance_score,
            last_check=datetime.now(),
            next_check=datetime.now() + timedelta(days=1),
            violations=violations,
            corrective_actions=corrective_actions,
            status="Compliant" if compliance_score >= 0.8 else "Non-compliant"
        )
    
    def generate_compliance_report(self,
                                 metrics: List[ComplianceMetrics]) -> pd.DataFrame:
        """
        Generate comprehensive compliance report
        
        Args:
            metrics: List of compliance metrics
            
        Returns:
            DataFrame with compliance report
        """
        report_data = []
        
        for metric in metrics:
            report_data.append({
                'framework': metric.framework,
                'requirement_id': metric.requirement_id,
                'compliance_score': metric.compliance_score,
                'status': metric.status,
                'violations': len(metric.violations),
                'corrective_actions': len(metric.corrective_actions),
                'last_check': metric.last_check,
                'next_check': metric.next_check
            })
            
        return pd.DataFrame(report_data)
    
    def monitor_regulatory_changes(self,
                                 current_requirements: List[ComplianceRequirement],
                                 new_requirements: List[ComplianceRequirement]) -> List[Dict]:
        """
        Monitor regulatory changes
        
        Args:
            current_requirements: Current compliance requirements
            new_requirements: New compliance requirements
            
        Returns:
            List of regulatory changes
        """
        changes = []
        
        # Convert to dictionaries for easier comparison
        current_dict = {req.requirement_id: req for req in current_requirements}
        new_dict = {req.requirement_id: req for req in new_requirements}
        
        # Check for new requirements
        for req_id, req in new_dict.items():
            if req_id not in current_dict:
                changes.append({
                    'type': 'new',
                    'requirement_id': req_id,
                    'description': req.description,
                    'effective_date': req.effective_date
                })
        
        # Check for modified requirements
        for req_id, req in new_dict.items():
            if req_id in current_dict:
                current_req = current_dict[req_id]
                if req.threshold != current_req.threshold:
                    changes.append({
                        'type': 'modified',
                        'requirement_id': req_id,
                        'old_threshold': current_req.threshold,
                        'new_threshold': req.threshold,
                        'effective_date': req.effective_date
                    })
        
        # Check for removed requirements
        for req_id, req in current_dict.items():
            if req_id not in new_dict:
                changes.append({
                    'type': 'removed',
                    'requirement_id': req_id,
                    'description': req.description
                })
        
        return changes
    
    def calculate_risk_score(self,
                           metrics: List[ComplianceMetrics]) -> float:
        """
        Calculate overall compliance risk score
        
        Args:
            metrics: List of compliance metrics
            
        Returns:
            Risk score (0-1)
        """
        if not metrics:
            return 1.0
        
        # Calculate weighted average of compliance scores
        weights = {
            RegulatoryFramework.MICA: 0.3,
            RegulatoryFramework.GENIUS: 0.3,
            RegulatoryFramework.FSB: 0.2,
            RegulatoryFramework.BIS: 0.1,
            RegulatoryFramework.FATF: 0.1
        }
        
        weighted_scores = [
            metric.compliance_score * weights.get(metric.framework, 0.1)
            for metric in metrics
        ]
        
        return 1.0 - sum(weighted_scores)

# Example usage
if __name__ == "__main__":
    # Initialize compliance engine
    compliance_engine = AdvancedCompliance()
    
    # Add compliance requirements
    mica_requirement = ComplianceRequirement(
        framework=RegulatoryFramework.MICA,
        requirement_id="MICA_001",
        description="Reserve requirements for stablecoins",
        threshold=1.0,
        monitoring_frequency="daily",
        reporting_frequency="monthly",
        effective_date=datetime.now(),
        jurisdiction="EU",
        category="Reserves"
    )
    
    genius_requirement = ComplianceRequirement(
        framework=RegulatoryFramework.GENIUS,
        requirement_id="GENIUS_001",
        description="KYC requirements for stablecoin issuers",
        threshold=0.95,
        monitoring_frequency="daily",
        reporting_frequency="monthly",
        effective_date=datetime.now(),
        jurisdiction="US",
        category="KYC"
    )
    
    compliance_engine.add_requirement(mica_requirement)
    compliance_engine.add_requirement(genius_requirement)
    
    # Check compliance
    mica_metrics = compliance_engine.check_mica_compliance(
        reserve_data={'ratio': 1.0},
        transaction_data={'amount': 500000}
    )
    
    genius_metrics = compliance_engine.check_genius_compliance(
        stablecoin_data={'reserve_ratio': 1.0},
        kyc_data={'completion_rate': 0.98}
    )
    
    # Generate report
    report = compliance_engine.generate_compliance_report([mica_metrics, genius_metrics])
    
    # Calculate risk score
    risk_score = compliance_engine.calculate_risk_score([mica_metrics, genius_metrics]) 