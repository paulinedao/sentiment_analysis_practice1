"""
Deployment of web app using Flask
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emot_detector():
    """
    Detect emotions in a given text
    """
    text_to_analyze = request.args.get("textToAnalyze")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again."

    emotion_scores = emotion_detector(text_to_analyze)

    if emotion_scores['dominant_emotion'] is None:
        return "Invalid text! Please try again."

    formatted_scores = ""
    for idx, (emotion, score) in enumerate(list(emotion_scores.items())[:-1]):
        if idx == len(emotion_scores) - 2:
            formatted_scores += f"and '{emotion}': {score}"
        else:
            formatted_scores += f"'{emotion}': {score}, "

    response = f"For the given statement, the system response is {formatted_scores}.\
        The dominant emotion is {emotion_scores['dominant_emotion']}."

    return response

@app.route("/")
def render_index_page():
    """Function to render HTML template"""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
