from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API details from environment variables
AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT")
AGENT_KEY = os.getenv("AGENT_KEY")


def create_app():
    app = Flask(__name__)
    CORS(app)

    # OpenAI client setup
    client = OpenAI(
        base_url=AGENT_ENDPOINT,
        api_key=AGENT_KEY,
    )

    @app.route("/predict", methods=["POST"])
    def predict_anomaly():
        try:
            # Parse JSON input
            data = request.get_json()
            cpu_usage = data.get("cpu_usage")
            cpu_temp = data.get("cpu_temp")

            if cpu_usage is None or cpu_temp is None:
                return jsonify({"error": "Invalid input. Provide 'cpu_usage' and 'cpu_temp'."}), 400

            # Send data to OpenAI agent
            response = client.chat.completions.create(
                model="n/a",
                messages=[{"role": "user", "content": f'{{"cpu_usage": {cpu_usage}, "cpu_temp": {cpu_temp}}}'}],
            )

            # Extract and return response
            prediction_response = response.choices[0].message.content
            return jsonify({
                "cpu_usage": cpu_usage,
                "cpu_temp": cpu_temp,
                "prediction": prediction_response
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
