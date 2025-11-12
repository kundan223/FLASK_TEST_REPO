from flask import Blueprint, request, jsonify, render_template
from database import get_db_connection
from prompts import analyze_transaction

fraud_routes = Blueprint('fraud_routes', __name__)

@fraud_routes.route('/predict', methods=['GET', 'POST'])
def predict_fraud():
    if request.method == 'POST':
        # Handle both form and JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                "user_name": request.form.get("user_name"),
                "amount": request.form.get("amount"),
                "location": request.form.get("location"),
                "device": request.form.get("device")
            }

        result = analyze_transaction(data)

        # Save result to DB
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO transactions (user_name, amount, location, device, result) VALUES (?, ?, ?, ?, ?)",
            (data["user_name"], data["amount"], data["location"], data["device"], result)
        )
        conn.commit()
        conn.close()

        # If HTML form, render a result page
        if not request.is_json:
            return render_template("result.html", user=data["user_name"], result=result)

        # If API request, return JSON
        return jsonify({"prediction": result})

    return jsonify({"error": "POST request required"})
