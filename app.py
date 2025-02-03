from flask import Flask, request, jsonify
import joblib
import numpy as np

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load the saved model and scaler
    model = joblib.load("./models/isolation_forest_model.pkl")
    scaler = joblib.load("./models/scaler.pkl")

    @app.route("/predict", methods=["POST"])
    def predict_anomaly():
        try:
            # Parse JSON input
            data = request.get_json()
            cpu_usage = data.get("cpu_usage")
            cpu_temp = data.get("cpu_temp")

            # Validate inputs
            if cpu_usage is None or cpu_temp is None:
                return jsonify({"error": "Invalid input. Provide 'cpu_usage' and 'cpu_temp'."}), 400

            # Prepare input for the model
            input_data = np.array([[cpu_usage, cpu_temp]])
            normalized_data = scaler.transform(input_data)

            # Make prediction
            prediction = model.predict(normalized_data)

            # Return result
            result = "Anomaly" if prediction[0] == -1 else "Normal"
            return jsonify({"cpu_usage": cpu_usage, "cpu_temp": cpu_temp, "prediction": result})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

# Create the Gunicorn-compatible application instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
