from flask import Flask, request, jsonify
import os
import traceback
from models import db, Mortgages
from credit_rating import CreditRating
import logging

LOGGER = logging.getLogger(__name__)

# Store DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "mortgages.db")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(DATABASE)}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/add_detail", methods=["POST"])
def add_detail():
    if request.is_json:
        data = request.get_json()

        credit_score = data.get("credit_score")
        loan_amt = data.get("loan_amt")
        property_value = data.get("property_value")
        annual_income = data.get("annual_income")
        debt_amt = data.get("debt_amt")
        loan_type = data.get("loan_type")
        property_type = data.get("property_type")

        LOGGER.info(f"Data submitted by user: {data}")

        mortgage_detail = Mortgages(
            credit_score=credit_score,
            loan_amount=loan_amt,
            property_value=property_value,
            annual_income=annual_income,
            debt_amount=debt_amt,
            loan_type=loan_type,
            property_type=property_type,
        )

        try:
            db.session.add(mortgage_detail)
            db.session.commit()
            # run credit_rating.py
            creditRating = CreditRating()
            credit_rating = creditRating.calculate_credit_rating(
                credit_score,
                loan_amt,
                property_value,
                annual_income,
                debt_amt,
                loan_type,
                property_type,
            )
            LOGGER.info(f"Credit Rating ::: {credit_rating}")
            return jsonify({"Credit Rating": credit_rating}), 201

        except ValueError as ve:
            LOGGER.error(f"Validation error: {ve}")
            return jsonify({"Error": str(ve)}), 400
        except TypeError as te:
            LOGGER.error(f"Type error: {te}")
            return jsonify({"Error": str(te)}), 400
        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"Error: {e}")
            LOGGER.error("Stack Trace:")
            traceback.print_exc()
            return jsonify({"Error": str(e)}), 500
    else:
        return jsonify({"Error": "Request is not JSON"}), 400


@app.route("/mortgages", methods=["GET"])
def get_mortgages():
    mortgages_detail = Mortgages.query.all()
    mortgages_list = [mortgage.to_dict() for mortgage in mortgages_detail]
    return jsonify(mortgages_list)


@app.route("/mortgages/<int:id>", methods=["DELETE"])
def delete_mortgages(id):
    record_id = Mortgages.query.get(id)
    if record_id:
        db.session.delete(record_id)
        db.session.commit()
        return "", 204
    else:
        return jsonify({"Message": "Record_id not found"}), 404


@app.route("/mortgages/<int:id>", methods=["PUT"])
def update_mortgages(id):
    record_id = Mortgages.query.get(id)
    if record_id:
        data = request.get_json()

        credit_score = data.get("credit_score", record_id.credit_score)
        loan_amt = data.get("loan_amt", record_id.loan_amount)
        property_value = data.get("property_value", record_id.property_value)
        annual_income = data.get("annual_income", record_id.annual_income)
        debt_amt = data.get("debt_amt", record_id.debt_amount)
        loan_type = data.get("loan_type", record_id.loan_type)
        property_type = data.get("property_type", record_id.property_type)

        record_id.credit_score = credit_score
        record_id.loan_amount = loan_amt
        record_id.property_value = property_value
        record_id.annual_income = annual_income
        record_id.debt_amt = debt_amt
        record_id.loan_type = loan_type
        record_id.property_type = property_type

        try:
            db.session.commit()
            creditRating = CreditRating()
            credit_rating = creditRating.calculate_credit_rating(
                credit_score,
                loan_amt,
                property_value,
                annual_income,
                debt_amt,
                loan_type,
                property_type,
            )
            LOGGER.info(f"Updated Credit Rating ::: {credit_rating}")
            return jsonify({"Credit Rating": credit_rating}), 200
        except Exception as e:
            db.session.rollback()
            LOGGER.error(f"Error: {e}")
            LOGGER.error("Stack Trace:")
            traceback.print_exc()
            return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
