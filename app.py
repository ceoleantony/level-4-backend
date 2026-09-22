from flask import Flask, jsonify, request
from flask_cors import CORS

from database import get_db_connection

app = Flask(__name__)
CORS(app)

db = get_db_connection()
scores_collection = db["scores"]

# Your routes
@app.route("/")
def home():
    return jsonify({
        "message": "Spot the Difference Backend is running!"
    })







@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():

    try:
        scores = scores_collection.find().sort([
            ("score", -1),
            ("completion_time", 1)
        ])

        leaderboard = []

        for score in scores:
            leaderboard.append({
                "id": str(score["_id"]),
                "username": score["username"],
                "score": score["score"],
                "completion_time": score["completion_time"]
            })

        return jsonify({
            "success": True,
            "leaderboard": leaderboard
        }), 200

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500
    
@app.route("/api/scores", methods=["POST"])
def save_score():

    try:
        data = request.get_json()

        username = data.get("username")
        score = data.get("score")
        completion_time = data.get("completion_time")

        if not username or score is None or completion_time is None:
            return jsonify({
                "success": False,
                "message": "Username, score and completion time are required."
            }), 400

        score_data = {
            "username": username,
            "score": score,
            "completion_time": completion_time
        }

        result = scores_collection.insert_one(score_data)

        return jsonify({
            "success": True,
            "message": "Score saved successfully.",
            "scoreId": str(result.inserted_id)
        }), 201

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# Start server LAST
if __name__ == "__main__":
    app.run(debug=True, port=5000)
   