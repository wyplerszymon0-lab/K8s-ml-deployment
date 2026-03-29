from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np

_model = None

def _load_model():
    global _model
    if _model is None:
        iris = load_iris()
        _model = RandomForestClassifier(n_estimators=100, random_state=42)
        _model.fit(iris.data, iris.target)
        print("Model trained on Iris dataset.")
    return _model

def predict(features: list) -> dict:
    model = _load_model()
    iris = load_iris()
    features_array = np.array(features).reshape(1, -1)
    prediction_index = model.predict(features_array)[0]
    confidence = float(np.max(model.predict_proba(features_array)))
    return {
        "class_index": int(prediction_index),
        "class_name": iris.target_names[prediction_index],
        "confidence": round(confidence, 4)
    }
