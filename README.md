# Residential Mortgage Securities (RMBS) Credit Rating

This project provides a complete solution for calculating the credit rating of Residential Mortgages.

The solution consists of three main components:
- **Frontend**: A React web interface for entering mortgage data, displaying validation errors, submitting the data to the backend, and displaying the credit rating and mortgage list.
- **Backend**: A Flask-based REST API that calculates the credit rating based on predefined business rules and stores/retrieves mortgage data using Flask-SQLAlchemy with a MySQL database.
- **Database**: A MySQL database for storing mortgage data with the necessary schema.

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:
```bash
git clone <repository-url>
cd credit_rating
```
### 2. Set Up the Frontend (React)

```bash
cd frontend
```
Install the required frontend dependencies:
```bash
npm install
```
Start the React development server:
```bash
npm start
```
The application will be accessible at http://localhost:3000.

### 3. Set Up the Backend (Flask)

```bash
cd backend
```
Create a virtual environment and activate it:
```bash
virtualenv env
source env/bin/activate
```
Install requirements.txt file to virtual end
```bash
pip install -r requirements.txt
```
Run the backend server:
```bash
python app.py
```

## Features

### Frontend:
- Input fields for mortgage data (credit score, loan amount, property value, etc.).
- Display of validation errors when data is invalid.
- Submission of data to backend for credit rating calculation.
- Display of calculated credit rating.

### Backend:
- POST API for calculating credit rating based on provided business logic.
- GET API for retrieving all stored mortgages from the database.

## Credit Rating Algorithm

The credit rating is calculated based on the following business rules:

### Loan-to-Value (LTV) Ratio:
- **LTV > 90%**: Add 2 points to the risk score.
- **LTV > 80%**: Add 1 point to the risk score.

### Debt-to-Income (DTI) Ratio:
- **DTI > 50%**: Add 2 points to the risk score.
- **DTI > 40%**: Add 1 point to the risk score.

### Credit Score:
- **Credit Score >= 700**: Subtract 1 point.
- **Credit Score >= 650 and < 700**: No change.
- **Credit Score < 650**: Add 1 point.

### Loan Type:
- **Fixed-rate loan**: Subtract 1 point.
- **Adjustable-rate loan**: Add 1 point.

### Property Type:
- **Single-family home**: No change.
- **Condo**: Add 1 point.

### Average Credit Score:
- **Average credit score >= 700**: Subtract 1 point.
- **Average credit score < 650**: Add 1 point.

### Final Rating:
- **Total risk score <= 2**: "AAA"
- **Total risk score between 3 and 5**: "BBB"
- **Total risk score > 5**: "C"



###  Testing
```bash
cd backend
python -m unittest tests/test_credit_rating.py
```
