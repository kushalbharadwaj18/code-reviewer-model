# from flask import Flask, request, jsonify
# from code_reviewer import AICodeReviewer

# app = Flask(__name__)

# reviewer = AICodeReviewer()

# @app.route("/review", methods=["POST"])
# def review():
#     data = request.get_json()

#     if not data or "code" not in data:
#         return jsonify({"error": "Missing 'code' field"}), 400

#     code = data["code"].strip()

#     if len(code) < 30:
#         return jsonify({
#             "error": "Code snippet too short or incomplete for review"
#         }), 400

#     review = reviewer.review_code(code)

#     return jsonify({
#         "review": review
#     })

# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "OK"})

# if __name__ == "__main__":
#     app.run(port=3000, debug=True)










from flask import Flask, request, jsonify
from code_reviewer import AICodeReviewer

app = Flask(__name__)

reviewer = AICodeReviewer()

@app.route("/review", methods=["POST"])
def review():
    data = request.get_json()

    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code' field"}), 400

    code = data["code"].strip()
    # language = data.get("language", "general")

    if len(code) < 30:
        return jsonify({
            "error": "Code snippet too short or incomplete for review"
        }), 400

    result = reviewer.review_code(code)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(port=3000, debug=True)




