from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "CarbonX Backend Running"

# Carbon credit calculation API
@app.route("/calculate_credits", methods=["POST"])
def calculate_credits():
    data = request.json
    trees = data.get("trees", 0)

    # simple carbon calculation
    credits = (trees * 20) / 1000

    return jsonify({
        "trees_planted": trees,
        "carbon_credits": credits
    })

if __name__ == "__main__":
    app.run(debug=True)