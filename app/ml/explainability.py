import shap
import numpy as np

class FraudExplainer:
    def __init__(self, model, feature_names):
        self.explainer = shap.TreeExplainer(model.model)
        self.feature_names = feature_names

    def explain(self, X):
        """
        Returns SHAP values for transactions
        """
        shap_values = self.explainer.shap_values(X)
        return shap_values
