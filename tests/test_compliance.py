import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from crew import ComplianceReport

def test_compliance_flag():
    result = ComplianceReport.parse_file("outputs/compliance_report.json")

    # Check that "compliant" is really a boolean
    assert isinstance(result.compliant, bool)

    # Just assert that the compliance flag is consistent with its own type
    # (True means valid, False means rejected)
    if result.compliant:
        print(f"✅ Order for {result.ticker} is compliant")
    else:
        print(f"❌ Order for {result.ticker} is NOT compliant")