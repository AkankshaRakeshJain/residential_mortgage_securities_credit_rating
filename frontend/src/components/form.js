import React, { useState, useEffect } from "react";

const Form = () => {
  const [formData, setFormData] = useState({
    credit_score: "",
    loan_amt: "",
    property_value: "",
    annual_income: "",
    debt_amt: "",
    loan_type: "",
    property_type: "",
  });

  const [errors, setErrors] = useState({});
  const [mortgages, setMortgages] = useState([]);
  const [creditRating, setCreditRating] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [globalError, setGlobalError] = useState("");

  useEffect(() => {
    fetchMortgages();
  }, []);

  const fetchMortgages = async () => {
    try {
      const response = await fetch("http://localhost:3000/mortgages");
      if (response.ok) {
        const data = await response.json();
        setMortgages(data);
      } else {
        console.error("Error fetching mortgages");
      }
    } catch (error) {
      console.error("Error fetching mortgages:", error);
    }
  };

  const isValidCreditScore = (credit_score) => {
    return parseInt(credit_score) >= 300 && parseInt(credit_score) <= 850;
  };

  const isValidNumber = (value) => {
    const number = parseFloat(value);
    return !isNaN(number) && number > 0;
  };

  const validateForm = () => {
    let newErrors = {};

    if (!formData.credit_score) {
      newErrors.credit_score = "Credit Score required";
    } else if (!isValidCreditScore(formData.credit_score)) {
      newErrors.credit_score = "An integer between 300 and 850.";
    }

    if (!formData.loan_amt) {
      newErrors.loan_amt = "Loan Amount is required";
    } else if (!isValidNumber(formData.loan_amt)) {
      newErrors.loan_amt =
        "The total loan amount of the mortgage (positive number).";
    }

    if (!formData.property_value) {
      newErrors.property_value = "Property Value required";
    } else if (!isValidNumber(formData.property_value)) {
      newErrors.property_value =
        "The value of the mortgaged property (positive number).";
    }

    if (!formData.annual_income) {
      newErrors.annual_income = "Annual Income required";
    } else if (!isValidNumber(formData.annual_income)) {
      newErrors.annual_income = "Annual Income must be a positive number.";
    }

    if (!formData.debt_amt) {
      newErrors.debt_amt = "Debt Amount required";
    } else if (!isValidNumber(formData.debt_amt)) {
      newErrors.debt_amt = "Debt Amount must be a positive number.";
    }

    if (!formData.loan_type) {
      newErrors.loan_type = "Loan Type is required";
    }
    if (!formData.property_type) {
      newErrors.property_type = "Property Type is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const isValid = validateForm();
    if (isValid) {
      setIsSubmitting(true);
      setGlobalError("");

      console.log("Form Submitted", formData);

      const mortgage_val = { ...formData };
      let response;

      try {
        if (formData.id) {
          response = await fetch(
            `http://localhost:3000/mortgages/${formData.id}`,
            {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(mortgage_val),
            },
          );
        } else {
          response = await fetch("http://localhost:3000/add_detail", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(mortgage_val),
          });
        }

        if (response.ok) {
          console.log("Form submitted", mortgage_val);
          const responseData = await response.json();
          console.log("Credit Rating:", responseData["Credit Rating"]);
          setCreditRating(responseData["Credit Rating"]);

          fetchMortgages();

          setFormData({
            credit_score: "",
            loan_amt: "",
            property_value: "",
            annual_income: "",
            debt_amt: "",
            loan_type: "",
            property_type: "",
          });
        } else {
          const errorData = await response.json();
          setGlobalError(errorData.Error || "Error submitting form");
        }
      } catch (error) {
        console.error("Error during form submission:", error);
        setGlobalError("There was an error submitting the form.");
      } finally {
        setIsSubmitting(false);
      }
    } else {
      console.log("Validation Failed");
      return;
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleDelete = async (id) => {
    const response = await fetch(`http://localhost:3000/mortgages/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      setMortgages(mortgages.filter((mortgage) => mortgage.id !== id));
    } else {
      console.log("Error deleting mortgage");
    }
  };

  const handleEdit = async (id) => {
    const mortgageToEdit = mortgages.find((mortgage) => mortgage.id === id);
    if (mortgageToEdit) {
      setFormData({
        id: mortgageToEdit.id,
        credit_score: mortgageToEdit.credit_score,
        loan_amt: mortgageToEdit.loan_amt,
        property_value: mortgageToEdit.property_value,
        annual_income: mortgageToEdit.annual_income,
        debt_amt: mortgageToEdit.debt_amt,
        loan_type: mortgageToEdit.loan_type,
        property_type: mortgageToEdit.property_type,
      });
      setCreditRating(null);
    }
  };

  return (
    <div>
      <form className="form_css" onSubmit={handleSubmit}>
        <div>
          <label>Credit Score: </label>
          <input
            type="number"
            name="credit_score"
            value={formData.credit_score}
            onChange={handleChange}
            placeholder="Value between 300-850"
          />
          {errors.credit_score && (
            <div className="error">{errors.credit_score}</div>
          )}
        </div>
        <div>
          <label>Loan amount: </label>
          <input
            type="number"
            name="loan_amt"
            value={formData.loan_amt}
            placeholder="Total loan amount"
            onChange={handleChange}
            step="any"
          />
          {errors.loan_amt && <div className="error">{errors.loan_amt}</div>}
        </div>
        <div>
          <label>Property value: </label>
          <input
            type="number"
            name="property_value"
            value={formData.property_value}
            placeholder="Value of the mortgaged property."
            onChange={handleChange}
            step="any"
          />
          {errors.property_value && (
            <div className="error">{errors.property_value}</div>
          )}
        </div>
        <div>
          <label>Annual income: </label>
          <input
            type="number"
            name="annual_income"
            value={formData.annual_income}
            placeholder="Borrower annual income."
            onChange={handleChange}
            step="any"
          />
          {errors.annual_income && (
            <div className="error">{errors.annual_income}</div>
          )}
        </div>
        <div>
          <label>Debt amount: </label>
          <input
            type="number"
            name="debt_amt"
            value={formData.debt_amt}
            placeholder="Borrower existing debt"
            onChange={handleChange}
            step="any"
          />
          {errors.debt_amt && <div className="error">{errors.debt_amt}</div>}
        </div>
        <div>
          <label>Loan Type: </label>
          <select
            name="loan_type"
            value={formData.loan_type}
            onChange={handleChange}
          >
            <option value="">Select Loan Type</option>
            <option value="fixed">Fixed</option>
            <option value="adjustable">Adjustable</option>
          </select>
          {errors.loan_type && <div className="error">{errors.loan_type}</div>}
        </div>
        <div>
          <label>Property Type: </label>
          <select
            name="property_type"
            value={formData.property_type}
            onChange={handleChange}
          >
            <option value="">Select Property Type</option>
            <option value="single_family">Single Family</option>
            <option value="condo">Condo</option>
          </select>
          {errors.property_type && (
            <div className="error">{errors.property_type}</div>
          )}
        </div>
        <div className="button-container">
          <button className="button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : "Submit"}
          </button>
        </div>
      </form>

      {globalError && <div className="error">{globalError}</div>}

      {creditRating && (
        <div className="credit-rating">
          <h3>Credit Rating: {creditRating}</h3>
        </div>
      )}

      <div>
        <h2>List of Mortgages</h2>
        {mortgages.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Credit Score</th>
                <th>Loan Amount</th>
                <th>Property Value</th>
                <th>Annual Income</th>
                <th>Debt Amount</th>
                <th>Loan Type</th>
                <th>Property Type</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {mortgages.map((mortgage) => (
                <tr key={mortgage.id}>
                  <td>{mortgage.credit_score}</td>
                  <td>{mortgage.loan_amt}</td>
                  <td>{mortgage.property_value}</td>
                  <td>{mortgage.annual_income}</td>
                  <td>{mortgage.debt_amt}</td>
                  <td>{mortgage.loan_type}</td>
                  <td>{mortgage.property_type}</td>
                  <td>
                    <button onClick={() => handleEdit(mortgage.id)}>
                      Edit
                    </button>
                    <button onClick={() => handleDelete(mortgage.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No mortgages found.</p>
        )}
      </div>
    </div>
  );
};

export default Form;
