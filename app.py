from flask import Flask, render_template, request, jsonify
import os
from googleapiclient import discovery
import google.auth

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "react-ef60e-firebase-adminsdk-hqoze-e399bdac16.json"  # Set your service account key path
credentials, _ = google.auth.default()
api_service = discovery.build('commentanalyzer', 'v1alpha1', credentials=credentials)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sort-lyrics", methods=["POST"])
def sort_lyrics():
    lyrics = request.form["lyrics"]
    lyrics_split = lyrics.split("\n")
    
    lyrics_scored = []
    for line in lyrics_split:
        if line:
            analyze_request = {
                "comment": {"text": line},
                "requestedAttributes": {"TOXICITY": {}},
            }
            response = api_service.comments().analyze(body=analyze_request).execute()
            toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            lyrics_scored.append({"text": line, "toxicity": toxicity_score})
    
    return jsonify(lyrics_scored)

if __name__ == "__main__":
    app.run(debug=True)
