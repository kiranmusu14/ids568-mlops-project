import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 1. Load the dataset (built-in to scikit-learn)
# This fetches data about California housing prices
print("Loading dataset...")
data = fetch_california_housing()
X = data.data
y = data.target

# 2. Split data (optional for this simple artifact, but good practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train a simple Linear Regression model
print("Training model...")
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Save the model as model.pkl
# This is the file you will verify in your assignment checklist
joblib.dump(model, 'model.pkl')

print("Success! 'model.pkl' has been created in your current directory.")
print(f"Model expects {X.shape[1]} features as input.")
print(f"Feature names: {data.feature_names}")