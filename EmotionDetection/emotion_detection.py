"""
Write the function to run emotion detection
"""
import json
import requests

def emotion_detector(text_to_analyze):
    """Function for emotion detection in a text"""
    if not text_to_analyze:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }
    
    try:
        response = requests.post(url, json=myobj, headers=header)
        data_dict = json.loads(response.text)

        if response.status_code == 200:
            key = "emotionPredictions"
            emotion_predictor = data_dict[key][0]['emotion']
            dominant_emotion = max(emotion_predictor, key=emotion_predictor.get)
            emotion_predictor['dominant_emotion'] = dominant_emotion
            emotion_response = {
                'anger': emotion_predictor['anger'],
                'disgust': emotion_predictor['disgust'],
                'fear': emotion_predictor['fear'],
                'joy': emotion_predictor['joy'],
                'sadness': emotion_predictor['sadness'],
                'dominant_emotion': emotion_predictor['dominant_emotion']
            }
        elif response.status_code == 400:
            emotion_response = {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        else:
            return {'error': f"Invalid text with status code {response.status_code}. Please try again!___"}
    except requests.exceptions.RequestException as e:
        return {'error': f"Request failed: {e}"}

    return emotion_response
    