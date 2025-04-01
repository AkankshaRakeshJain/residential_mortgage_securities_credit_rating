from sqlalchemy.sql import func
from models import db, Mortgages


class CreditRating:
    def calculate_credit_rating(
        self,
        credit_score,
        loan_amount,
        property_value,
        annual_income,
        debt_amount,
        loan_type,
        property_type,
    ):
        """
        calculated credit rating : AAA, BBB, or C
        """
        risk_score = 0

        # LTV is the ratio of the loan amount to the property value.
        ltv_ratio = (float(loan_amount) / float(property_value)) * 100
        if ltv_ratio > 90:
            risk_score += 2
        elif ltv_ratio > 80:
            risk_score += 1

        # DTI is the ratio of the borrower’s existing debt to their annual income.
        dti_ratio = (float(debt_amount) / float(annual_income)) * 100
        if dti_ratio > 50:
            risk_score += 2
        elif dti_ratio > 40:
            risk_score += 1

        # The credit score indicates the borrower's ability to repay the loan.
        credit_score = float(credit_score)
        if credit_score >= 700:
            risk_score -= 1
        elif credit_score >= 650 and credit_score < 700:
            pass
        elif credit_score < 650:
            risk_score += 1

        # Loan Type
        if loan_type == "Fixed":
            risk_score -= 1
        elif loan_type == "Adjustable":
            risk_score += 1

        # Property Type
        if property_type == "Single Family":
            pass
        elif property_type == "Condo":
            risk_score += 1

        # Average Credit Score
        average_credit_score = db.session.query(
            db.func.avg(Mortgages.credit_score)
        ).scalar()
        print(f"Average Credit Score ::: {average_credit_score}")
        if average_credit_score is not None:
            if average_credit_score >= 700:
                risk_score -= 1
            elif average_credit_score < 650:
                risk_score += 1

        if risk_score <= 2:
            return "AAA"
        elif 3 <= risk_score <= 5:
            return "BBB"
        else:
            return "C"
