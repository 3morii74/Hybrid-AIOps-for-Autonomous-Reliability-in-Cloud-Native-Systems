import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
from datetime import datetime

class HealingBrain:
    """
    ML-based brain that learns patterns and recommends healing actions
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'cpu_usage',
            'memory_usage',
            'error_count',
            'uptime',
            'hour_of_day'
        ]
        
    def generate_training_data(self, n_samples=1000):
        """Generate synthetic training data"""
        print(f"📊 Generating {n_samples} training samples...")
        
        data = []
        
        for _ in range(n_samples):
            cpu = np.random.randint(0, 100)
            memory = np.random.randint(0, 100)
            errors = np.random.randint(0, 20)
            uptime = np.random.randint(0, 86400)  # seconds in a day
            hour = np.random.randint(0, 24)
            
            # Determine healing action based on rules
            # 0 = no action, 1 = reset_errors, 2 = restart_service
            if errors > 10 or (cpu > 90 and memory > 90):
                action = 2  # restart_service
            elif errors > 5 or cpu > 80 or memory > 80:
                action = 1  # reset_errors
            else:
                action = 0  # no action
            
            data.append({
                'cpu_usage': cpu,
                'memory_usage': memory,
                'error_count': errors,
                'uptime': uptime,
                'hour_of_day': hour,
                'healing_action': action
            })
        
        return pd.DataFrame(data)
    
    def train(self, df=None):
        """Train the healing brain model"""
        print("\n🧠 Training Healing Brain...")
        
        # Generate data if not provided
        if df is None:
            df = self.generate_training_data()
        
        # Prepare features and target
        X = df[self.feature_names]
        y = df['healing_action']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"  Training samples: {len(X_train)}")
        print(f"  Test samples: {len(X_test)}")
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✅ Training complete!")
        print(f"  Accuracy: {accuracy:.2%}")
        
        print("\n📋 Classification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=['No Action', 'Reset Errors', 'Restart Service']
        ))
        
        # Feature importance
        print("\n🔍 Feature Importance:")
        for name, importance in zip(self.feature_names, self.model.feature_importances_):
            print(f"  {name}: {importance:.3f}")
        
        return accuracy
    
    def predict_action(self, metrics):
        """Predict healing action based on metrics"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Prepare features
        features = pd.DataFrame([{
            'cpu_usage': metrics.get('cpu_usage', 0),
            'memory_usage': metrics.get('memory_usage', 0),
            'error_count': metrics.get('error_count', 0),
            'uptime': metrics.get('uptime', 0),
            'hour_of_day': datetime.now().hour
        }])
        
        # Predict
        action = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        action_names = ['no_action', 'reset_errors', 'restart_service']
        
        return {
            'recommended_action': action_names[action],
            'confidence': float(probabilities[action]),
            'probabilities': {
                name: float(prob)
                for name, prob in zip(action_names, probabilities)
            }
        }
    
    def save_model(self, filepath='healing_brain.pkl'):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save!")
        
        joblib.dump(self.model, filepath)
        print(f"\n💾 Model saved to: {filepath}")
    
    def load_model(self, filepath='healing_brain.pkl'):
        """Load trained model"""
        self.model = joblib.load(filepath)
        print(f"\n📂 Model loaded from: {filepath}")

def main():
    """Main training script"""
    print("="*60)
    print("🧠 HEALING BRAIN TRAINING SYSTEM")
    print("="*60)
    
    brain = HealingBrain()
    
    # Train the model
    accuracy = brain.train()
    
    # Save the model
    brain.save_model('healing_brain.pkl')
    
    # Test prediction
    print("\n🧪 Testing prediction with sample metrics:")
    test_metrics = {
        'cpu_usage': 85,
        'memory_usage': 75,
        'error_count': 7,
        'uptime': 3600
    }
    
    print(f"  Input: {json.dumps(test_metrics, indent=2)}")
    
    prediction = brain.predict_action(test_metrics)
    print(f"\n  Prediction: {json.dumps(prediction, indent=2)}")
    
    print("\n" + "="*60)
    print("✅ Training complete! Model ready for use.")
    print("="*60)

if __name__ == '__main__':
    main()