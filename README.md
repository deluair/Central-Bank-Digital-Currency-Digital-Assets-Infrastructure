# Central Bank Digital Currency & Digital Assets Infrastructure (CBDCDAI)

A comprehensive platform for simulating, analyzing, and managing Central Bank Digital Currencies (CBDCs) and digital assets infrastructure.

## Overview

CBDCDAI provides a sophisticated framework for:
- Economic modeling and simulation of CBDC impacts
- Risk assessment and monitoring
- Regulatory compliance tracking
- Cross-border payment analysis
- Financial stability assessment

## Features

### Economic Simulation
- IS-LM model adaptation for CBDC
- Phillips Curve analysis
- Taylor Rule implementation
- Money multiplier effects
- Monetary policy impact simulation

### Risk Analytics
- Network risk analysis
- Liquidity risk modeling
- Operational risk assessment
- Systemic risk analysis
- Stress testing capabilities

### Regulatory Compliance
- Multi-jurisdictional compliance tracking
- Automated regulatory reporting
- Compliance risk scoring
- Regulatory change monitoring
- Support for major frameworks (MiCA, GENIUS Act, FSB, BIS, FATF)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/deluair/Central-Bank-Digital-Currency-Digital-Assets-Infrastructure.git
cd Central-Bank-Digital-Currency-Digital-Assets-Infrastructure
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Economic Models
```python
from cbdcdai.simulation.economic_models import EconomicModels, EconomicParameters

# Initialize models
params = EconomicParameters(
    natural_rate=0.02,
    inflation_target=0.02,
    output_gap_weight=0.5,
    inflation_weight=1.5,
    money_velocity=1.5,
    fiscal_multiplier=1.0
)
models = EconomicModels(params)

# Run simulation
results = models.simulate_monetary_impact(
    initial_conditions={
        'interest_rate': 0.02,
        'inflation': 0.02,
        'output': 1000,
        'potential_output': 1000,
        'unemployment': 0.05,
        'cbdc_adoption': 0.1,
        'reserve_ratio': 0.1,
        'currency_ratio': 0.2
    },
    policy_shock=0.01,
    periods=12
)
```

### Risk Assessment
```python
from cbdcdai.risk.advanced_risk_models import AdvancedRiskModels

# Initialize risk models
risk_models = AdvancedRiskModels()

# Calculate network risk
network_metrics = risk_models.calculate_network_risk(adjacency_matrix)

# Assess systemic risk
systemic_risk = risk_models.assess_systemic_risk(
    network_metrics,
    liquidity_metrics,
    operational_risk=0.2
)
```

### Compliance Monitoring
```python
from cbdcdai.compliance.advanced_compliance import AdvancedCompliance

# Initialize compliance engine
compliance_engine = AdvancedCompliance()

# Check MiCA compliance
metrics = compliance_engine.check_mica_compliance(
    reserve_data={'ratio': 1.0},
    transaction_data={'amount': 500000}
)

# Generate compliance report
report = compliance_engine.generate_compliance_report([metrics])
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on research from the IMF, BIS, and major central banks
- Incorporates insights from Project mBridge and other CBDC initiatives
- Aligned with regulatory frameworks including MiCA and the GENIUS Act 