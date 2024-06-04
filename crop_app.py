import joblib
import traceback  # Ensure this import statement is present
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/form', methods=['POST'])
def brain():
    if request.method == 'POST':
        try:
            # Get input data from the JSON request
            data = request.get_json()

            # Validate input data
            for key in ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Ph', 'Rainfall']:
                if key not in data or not isinstance(data[key], (int, float)):
                    return jsonify({'error': f'Invalid or missing value for {key}.'}), 400

            # Prepare input data for prediction
            input_data = [[data['Nitrogen'], data['Phosphorus'], data['Potassium'], data['Temperature'],
                           data['Humidity'], data['Ph'], data['Rainfall']]]

            # Load the machine learning model
            model = joblib.load('crop_app2.pkl')

            # Make prediction using the loaded model
            prediction = model.predict(input_data)

            # Return prediction as JSON response
            
           # result = {'prediction': float(prediction[0])}
            float_prediction = prediction[0]
             
            result = {'prediction': float_prediction}
            return jsonify(result)

        except Exception as e:
            # Handle exceptions and return error response
            traceback.print_exc()
            return jsonify({'error': 'An error occurred during prediction.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
