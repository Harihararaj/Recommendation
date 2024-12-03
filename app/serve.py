from pyspark.mllib.recommendation import MatrixFactorizationModel
from pyspark.sql import SparkSession
from pyspark import SparkContext
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Initialize Spark and load the model
spark = SparkSession.builder.appName("ALSModelInference").getOrCreate()
sc = SparkContext.getOrCreate()
model_path = "/app/als_model"
model = MatrixFactorizationModel.load(sc, model_path)

# Health check endpoint
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "healthy"}), 200

# Inference endpoint
@app.route('/invocations', methods=['POST'])
def invocations():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        num_recommendations = data.get("num_recommendations", 5)
        recommendations = model.recommendProducts(user_id, num_recommendations)
        results = [{"product_id": rec.product, "rating": rec.rating} for rec in recommendations]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
