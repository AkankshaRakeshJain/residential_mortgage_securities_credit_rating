from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.sql import func

db = SQLAlchemy()
TIMEZONE = 'Asia/Kolkata'


class Mortgages(db.Model):
    __tablename__ = 'mortgages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    credit_score = db.Column(db.Integer)
    loan_amount = db.Column(db.Integer, nullable=False)
    property_value = db.Column(db.Integer, nullable=False)
    annual_income = db.Column(db.Integer, nullable=False)
    debt_amount = db.Column(db.Integer, nullable=False)
    loan_type = db.Column(
        Enum('fixed', 'adjustable', name='loan_type'), nullable=False
    )
    property_type = db.Column(
        Enum('single_family', 'condo', name='property_type'), nullable=False
    )
    created_at = db.Column(
        db.TIMESTAMP, default=func.current_timestamp(), nullable=False
    )

    def __init__(
        self,
        credit_score,
        loan_amount,
        property_value,
        annual_income,
        debt_amount,
        loan_type,
        property_type,
    ):
        self.credit_score = credit_score
        self.loan_amount = loan_amount
        self.property_value = property_value
        self.annual_income = annual_income
        self.debt_amount = debt_amount
        self.loan_type = loan_type
        self.property_type = property_type

    def __repr__(self):
        return f"<Mortgage {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "credit_score": self.credit_score,
            "loan_amt": self.loan_amount,
            "property_value": self.property_value,
            "annual_income": self.annual_income,
            "debt_amt": self.debt_amount,
            "loan_type": self.loan_type,
            "property_type": self.property_type,
        }