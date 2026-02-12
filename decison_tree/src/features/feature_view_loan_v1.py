from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_loan_v1"

FEATURE_VIEW_DESCRIPTION = """
Decision tree feature view for loan default prediction.
Contains income, age, credit history and encoded categorical signals.
"""

RAW_TABLE = "loan_default_raw"
TARGET_COLUMN = "Default"

FEATURES = {
    "age": {"source_column": "Age", "data_type": "numeric"},
    "income": {"source_column": "Income", "data_type": "numeric"},
    "loan_amount": {"source_column": "LoanAmount", "data_type": "numeric"},
    "credit_score": {"source_column": "CreditScore", "data_type": "numeric"},
    "months_employed": {"source_column": "MonthsEmployed", "data_type": "numeric"},
    "num_credit_lines": {"source_column": "NumCreditLines", "data_type": "numeric"},
    "interest_rate": {"source_column": "InterestRate", "data_type": "numeric"},
    "loan_term": {"source_column": "LoanTerm", "data_type": "numeric"},
    "dti_ratio": {"source_column": "DTIRatio", "data_type": "numeric"},
}

def create_feature_view():

    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description="Loan decision tree features",
    )

    for name, meta in FEATURES.items():
        registry_feature(
            feature_name=name,
            feature_view=FEATURE_VIEW_NAME,
            description=name,
            data_type=meta["data_type"],
            source_column=meta["source_column"],
            transformation="identity",
        )

    sql = f"""
CREATE TABLE {FEATURE_VIEW_NAME} AS
SELECT
    "Age" AS age,
    "Income" AS income,
    "LoanAmount" AS loan_amount,
    "CreditScore" AS credit_score,
    "MonthsEmployed" AS months_employed,
    "NumCreditLines" AS num_credit_lines,
    "InterestRate" AS interest_rate,
    "LoanTerm" AS loan_term,
    "DTIRatio" AS dti_ratio,

    CASE WHEN "Education" = 'Graduate' THEN 1 ELSE 0 END AS education_code,
    CASE WHEN "EmploymentType" = 'Full-time' THEN 1 ELSE 0 END AS employment_code,
    CASE WHEN "HasMortgage" = 'Yes' THEN 1 ELSE 0 END AS has_mortgage,
    CASE WHEN "HasDependents" = 'Yes' THEN 1 ELSE 0 END AS has_dependents,
    CASE WHEN "HasCoSigner" = 'Yes' THEN 1 ELSE 0 END AS has_cosigner,

    "Default" AS target
FROM loan_default_raw
WHERE "Default" IS NOT NULL;
"""

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {FEATURE_VIEW_NAME};"))
        conn.execute(text(sql))

    print(f"Feature view created: {FEATURE_VIEW_NAME}")


if __name__ == "__main__":
    create_feature_view()