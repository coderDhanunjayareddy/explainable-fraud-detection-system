from sklearn.ensemble import IsolationForest
import numpy as np

class FraudAnomalyModel:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.1,   # Assume 10% anomalies
            random_state=42
        )

    def train(self, X):
        """
        Train the anomaly detection model
        """
        self.model.fit(X)

    def predict(self, X):
        """
        Returns:
        - anomaly_score (float)
        - is_suspicious (bool)
        """
        scores = self.model.decision_function(X)
        predictions = self.model.predict(X)

        # Isolation Forest outputs:
        # -1 → anomaly
        #  1 → normal
        is_suspicious = predictions == -1

        return scores, is_suspicious
