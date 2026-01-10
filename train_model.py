import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

# Import gradient boosting models
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    print("⚠️ XGBoost not available. Install with: pip install xgboost")
    XGBOOST_AVAILABLE = False

try:
    from lightgbm import LGBMClassifier
    LIGHTGBM_AVAILABLE = True
except ImportError:
    print("⚠️ LightGBM not available. Install with: pip install lightgbm")
    LIGHTGBM_AVAILABLE = False



# ✅ Normalization helper
def normalize(text):
    return text.lower().replace('-', ' ').strip()

# ✅ Load and preprocess the dataset
def load_dataset():
    try:
        df = pd.read_csv('dataset/career_data.csv')

        # Normalize
        df['Skills'] = df['Skills'].str.split(', ').apply(lambda lst: [normalize(skill) for skill in lst])
        df['Interests'] = df['Interests'].str.split(', ').apply(lambda lst: [normalize(interest) for interest in lst])
        df['Career'] = df['Career'].str.strip()
        df['Description'] = df['Description'].str.strip()

        print(f"✅ Loaded {len(df)} entries")
        print("📊 Career distribution BEFORE balancing:\n", df['Career'].value_counts())
        return df
    except FileNotFoundError:
        print("❌ File 'career_data.csv' not found.")
        return None

# ✅ Balance dataset manually (oversampling)
def balance_dataset(df):
    max_count = df['Career'].value_counts().max()
    balanced_df = pd.DataFrame()

    for career, group in df.groupby('Career'):
        samples = group.sample(max_count, replace=True, random_state=42)
        balanced_df = pd.concat([balanced_df, samples], axis=0)

    print("📊 Career distribution AFTER balancing:\n", balanced_df['Career'].value_counts())
    return balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

# ✅ Enhanced training with multiple models and hyperparameter tuning
def train_single_model(model_name, model, X_train, y_train, X_test, y_test, use_grid_search=False, label_encoder=None):
    """Train a single model with optional hyperparameter tuning"""
    print(f"\n🤖 Training {model_name}...")
    
    # For tree-based models that need numeric labels (XGBoost, LightGBM)
    needs_numeric_labels = model_name in ["XGBoost", "LightGBM"]
    
    if needs_numeric_labels and label_encoder is not None:
        # Encode labels
        y_train_encoded = label_encoder.transform(y_train)
        y_test_encoded = label_encoder.transform(y_test)
    else:
        y_train_encoded = y_train
        y_test_encoded = y_test
    
    if use_grid_search:
        print(f"   Performing hyperparameter tuning...")
        # Define hyperparameter grids based on model type
        if model_name == "RandomForest":
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            }
        elif model_name == "XGBoost" and XGBOOST_AVAILABLE:
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.3],
                'subsample': [0.8, 1.0]
            }
        elif model_name == "LightGBM" and LIGHTGBM_AVAILABLE:
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.3],
                'num_leaves': [31, 63]
            }
        else:
            param_grid = {}
        
        if param_grid:
            grid_search = GridSearchCV(
                model, param_grid, cv=3, scoring='accuracy',
                n_jobs=-1, verbose=0
            )
            grid_search.fit(X_train, y_train_encoded)
            model = grid_search.best_estimator_
            print(f"   Best parameters: {grid_search.best_params_}")
        else:
            model.fit(X_train, y_train_encoded)
    else:
        model.fit(X_train, y_train_encoded)
    
    # Evaluate
    y_pred = model.predict(X_test)
    
    # Decode predictions if needed
    if needs_numeric_labels and label_encoder is not None:
        y_pred_decoded = label_encoder.inverse_transform(y_pred)
        accuracy = accuracy_score(y_test, y_pred_decoded)
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred_decoded, average='weighted', zero_division=0
        )
    else:
        accuracy = accuracy_score(y_test_encoded, y_pred)
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test_encoded, y_pred, average='weighted', zero_division=0
        )
    
    print(f"✅ {model_name} Results:")
    print(f"   Accuracy: {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall: {recall:.4f}")
    print(f"   F1-Score: {f1:.4f}")
    
    # Return model
    return model, accuracy, precision, recall, f1

def perform_cross_validation(model_name, model, X, y, cv=5):
    """Perform k-fold cross-validation with stratification handling"""
    print(f"\n🔄 Performing cross-validation for {model_name}...")
    
    # Check if we have enough samples per class for stratified CV
    from collections import Counter
    class_counts = Counter(y)
    min_samples = min(class_counts.values())
    
    # Adjust cv folds if needed
    if min_samples < cv:
        cv = max(2, min_samples)
        print(f"   Adjusted to {cv}-fold CV due to class size constraints")
    
    try:
        cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy', n_jobs=-1)
        print(f"   CV Scores: {cv_scores}")
        print(f"   Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        return cv_scores
    except Exception as e:
        print(f"   ⚠️ Cross-validation skipped: {str(e)}")
        return None

# ✅ Main training function with enhanced features
def train_career_model(use_hyperparameter_tuning=False, use_ensemble=True):
    df = load_dataset()
    if df is None:
        return None

    # Combine features
    df['combined_features'] = df['Interests'] + df['Skills']

    # Encode features
    mlb = MultiLabelBinarizer()
    X_encoded = mlb.fit_transform(df['combined_features'])
    y = df['Career']

    print(f"✅ Feature matrix shape: {X_encoded.shape}")
    print(f"✅ Unique careers: {y.nunique()}")

    # Balance the dataset
    df_encoded = pd.DataFrame(X_encoded, columns=mlb.classes_)
    df_encoded['Career'] = y.values
    df_balanced = balance_dataset(df_encoded)

    X = df_balanced.drop(columns=['Career']).values
    y_balanced = df_balanced['Career']

    # Create label encoder for all careers (needed for XGBoost/LightGBM)
    label_encoder = LabelEncoder()
    label_encoder.fit(y_balanced)  # Fit on all careers
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_balanced, test_size=0.2, random_state=42)

    # Dictionary to store all trained models
    models = {}
    model_scores = {}
    
    # Train RandomForest
    rf_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    rf_result = train_single_model(
        "RandomForest", rf_model, X_train, y_train, X_test, y_test,
        use_grid_search=use_hyperparameter_tuning, label_encoder=label_encoder
    )
    rf_model, rf_acc, rf_prec, rf_rec, rf_f1 = rf_result
    models['RandomForest'] = rf_model
    model_scores['RandomForest'] = {
        'accuracy': rf_acc, 'precision': rf_prec, 
        'recall': rf_rec, 'f1': rf_f1
    }
    
    # Perform cross-validation for RandomForest
    perform_cross_validation("RandomForest", rf_model, X, y_balanced)
    
    # Train XGBoost if available
    if XGBOOST_AVAILABLE:
        xgb_model = XGBClassifier(n_estimators=200, random_state=42, n_jobs=-1, eval_metric='mlogloss')
        xgb_result = train_single_model(
            "XGBoost", xgb_model, X_train, y_train, X_test, y_test,
            use_grid_search=use_hyperparameter_tuning, label_encoder=label_encoder
        )
        xgb_model, xgb_acc, xgb_prec, xgb_rec, xgb_f1 = xgb_result
        models['XGBoost'] = xgb_model
        model_scores['XGBoost'] = {
            'accuracy': xgb_acc, 'precision': xgb_prec,
            'recall': xgb_rec, 'f1': xgb_f1
        }
        
        # Perform cross-validation for XGBoost
        # For XGBoost, need to encode labels for CV
        y_encoded = label_encoder.transform(y_balanced)
        xgb_cv_model = XGBClassifier(n_estimators=200, random_state=42, n_jobs=-1, eval_metric='mlogloss')
        perform_cross_validation("XGBoost", xgb_cv_model, X, y_encoded)
    
    # Train LightGBM if available
    if LIGHTGBM_AVAILABLE:
        lgbm_model = LGBMClassifier(n_estimators=200, random_state=42, n_jobs=-1, verbose=-1)
        lgbm_result = train_single_model(
            "LightGBM", lgbm_model, X_train, y_train, X_test, y_test,
            use_grid_search=use_hyperparameter_tuning, label_encoder=label_encoder
        )
        lgbm_model, lgbm_acc, lgbm_prec, lgbm_rec, lgbm_f1 = lgbm_result
        models['LightGBM'] = lgbm_model
        model_scores['LightGBM'] = {
            'accuracy': lgbm_acc, 'precision': lgbm_prec,
            'recall': lgbm_rec, 'f1': lgbm_f1
        }
        
        # Perform cross-validation for LightGBM
        y_encoded = label_encoder.transform(y_balanced)
        lgbm_cv_model = LGBMClassifier(n_estimators=200, random_state=42, n_jobs=-1, verbose=-1)
        perform_cross_validation("LightGBM", lgbm_cv_model, X, y_encoded)
    
    # Create ensemble model if multiple models are available and ensemble is enabled
    ensemble_model = None
    if use_ensemble and len(models) > 1:
        print(f"\n🎯 Creating Ensemble Voting Classifier with {len(models)} models...")
        # For ensemble, we need models that work with string labels (RandomForest only)
        rf_only_models = {name: model for name, model in models.items() if name == 'RandomForest'}
        
        if len(rf_only_models) > 0:
            estimators = [(name, model) for name, model in rf_only_models.items()]
            ensemble_model = VotingClassifier(estimators=estimators, voting='soft', n_jobs=-1)
            ensemble_model.fit(X_train, y_train)
            
            # Evaluate ensemble
            y_pred_ensemble = ensemble_model.predict(X_test)
            ensemble_acc = accuracy_score(y_test, y_pred_ensemble)
            ensemble_prec, ensemble_rec, ensemble_f1, _ = precision_recall_fscore_support(
                y_test, y_pred_ensemble, average='weighted', zero_division=0
            )
            
            print(f"✅ Ensemble Model Results:")
            print(f"   Accuracy: {ensemble_acc:.4f}")
            print(f"   Precision: {ensemble_prec:.4f}")
            print(f"   Recall: {ensemble_rec:.4f}")
            print(f"   F1-Score: {ensemble_f1:.4f}")
            
            models['Ensemble'] = ensemble_model
            model_scores['Ensemble'] = {
                'accuracy': ensemble_acc, 'precision': ensemble_prec,
                'recall': ensemble_rec, 'f1': ensemble_f1
            }
    
    # Print summary
    print("\n" + "="*60)
    print("📊 MODEL PERFORMANCE SUMMARY")
    print("="*60)
    for name, scores in model_scores.items():
        print(f"{name:15} | Acc: {scores['accuracy']:.4f} | Prec: {scores['precision']:.4f} | "
              f"Rec: {scores['recall']:.4f} | F1: {scores['f1']:.4f}")
    print("="*60)
    
    # Select best model based on F1-score
    best_model_name = max(model_scores, key=lambda x: model_scores[x]['f1'])
    best_model = models[best_model_name]
    print(f"\n🏆 Best model: {best_model_name} (F1-Score: {model_scores[best_model_name]['f1']:.4f})")

    # Get detailed classification report for best model
    if best_model_name in ["XGBoost", "LightGBM"]:
        y_test_encoded = label_encoder.transform(y_test)
        y_pred_best = best_model.predict(X_test)
        y_pred_best_decoded = label_encoder.inverse_transform(y_pred_best)
        print("\n📄 Detailed Classification Report (Best Model - showing first 20 classes):")
        report = classification_report(y_test, y_pred_best_decoded, zero_division=0)
        print('\n'.join(report.split('\n')[:25]))  # Limit output
    else:
        y_pred_best = best_model.predict(X_test)
        print("\n📄 Detailed Classification Report (Best Model - showing first 20 classes):")
        report = classification_report(y_test, y_pred_best, zero_division=0)
        print('\n'.join(report.split('\n')[:25]))  # Limit output

    # Map descriptions
    description_map = {normalize(career): desc for career, desc in zip(df['Career'], df['Description'])}

    # Save all models
    os.makedirs('model', exist_ok=True)
    
    # Save individual models
    for model_name, model in models.items():
        # Add label encoder for models that need it
        if model_name in ["XGBoost", "LightGBM"]:
            model_to_save = (model, label_encoder)
        else:
            model_to_save = model
            
        model_package = {
            'classifier': model_to_save,
            'feature_encoder': mlb,
            'feature_names': list(mlb.classes_),
            'careers': list(y.unique()),
            'descriptions': description_map,
            'model_scores': model_scores[model_name],
            'model_name': model_name
        }
        
        filename = f'model/career_model_{model_name.lower()}.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(model_package, f)
        print(f"✅ Saved {model_name} model to {filename}")
    
    # Save the best model as the default
    if best_model_name in ["XGBoost", "LightGBM"]:
        best_model_to_save = (best_model, label_encoder)
    else:
        best_model_to_save = best_model
        
    best_model_package = {
        'classifier': best_model_to_save,
        'feature_encoder': mlb,
        'feature_names': list(mlb.classes_),
        'careers': list(y.unique()),
        'descriptions': description_map,
        'model_scores': model_scores[best_model_name],
        'model_name': best_model_name,
        'all_model_scores': model_scores
    }
    
    with open('model/career_model.pkl', 'wb') as f:
        pickle.dump(best_model_package, f)
    print(f"\n✅ Best model ({best_model_name}) saved as default to model/career_model.pkl")
    
    return best_model_package

# ✅ Function to make predictions with confidence scores
def predict_with_confidence(model_package, skills, interests, top_k=5):
    """
    Predict careers with confidence scores
    
    Args:
        model_package: Trained model package
        skills: List of skills
        interests: List of interests
        top_k: Number of top predictions to return
        
    Returns:
        List of tuples (career, confidence, description)
    """
    # Normalize inputs
    skills = [normalize(s) for s in skills]
    interests = [normalize(i) for i in interests]
    combined_features = skills + interests
    
    # Encode features
    mlb = model_package['feature_encoder']
    X = mlb.transform([combined_features])
    
    # Get predictions with probabilities
    classifier = model_package['classifier']
    
    # Check if classifier supports predict_proba
    if hasattr(classifier, 'predict_proba'):
        probabilities = classifier.predict_proba(X)[0]
        classes = classifier.classes_
        
        # Get top k predictions
        top_indices = np.argsort(probabilities)[::-1][:top_k]
        
        predictions = []
        for idx in top_indices:
            career = classes[idx]
            confidence = probabilities[idx]
            description = model_package['descriptions'].get(normalize(career), "No description available")
            predictions.append((career, confidence, description))
        
        return predictions
    else:
        # Fallback for classifiers without predict_proba
        prediction = classifier.predict(X)[0]
        description = model_package['descriptions'].get(normalize(prediction), "No description available")
        return [(prediction, 1.0, description)]

# ✅ Execute when run directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train career recommendation model')
    parser.add_argument('--tune', action='store_true', 
                        help='Enable hyperparameter tuning (slower but better results)')
    parser.add_argument('--no-ensemble', action='store_true',
                        help='Disable ensemble model training')
    
    args = parser.parse_args()
    
    print("🚀 Starting enhanced career model training...")
    print("="*60)
    
    model_package = train_career_model(
        use_hyperparameter_tuning=args.tune,
        use_ensemble=not args.no_ensemble
    )
    
    if model_package:
        print("\n🎉 Training complete!")
        print("="*60)
        
        # Test prediction with confidence scores
        print("\n🧪 Testing prediction with confidence scores...")
        test_skills = ["python", "machine learning", "tensorflow"]
        test_interests = ["data analysis", "ai"]
        
        predictions = predict_with_confidence(model_package, test_skills, test_interests, top_k=5)
        print(f"\nTest input: Skills={test_skills}, Interests={test_interests}")
        print("\nTop 5 Career Predictions:")
        for i, (career, confidence, desc) in enumerate(predictions, 1):
            print(f"{i}. {career} ({confidence*100:.2f}% confidence)")
            print(f"   Description: {desc[:100]}...")
    else:
        print("❌ Training failed!")
    
    print("="*60)