import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os

# Load dataset
df = pd.read_csv("yield_df.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)
df.drop_duplicates(inplace=True)

# Reorder columns
col = ['Year','average_rain_fall_mm_per_year','pesticides_tonnes', 'avg_temp','Area', 'Item', 'hg/ha_yield']
df = df[col]

# Split features and target
X = df.drop('hg/ha_yield', axis=1)
y = df['hg/ha_yield']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=True)

# Preprocessing
ohe = OneHotEncoder(drop='first')
scale = StandardScaler()

preprocesser = ColumnTransformer(
    transformers=[
        ('StandardScale', scale, [0,1,2,3]),
        ('OneHotEncode', ohe, [4,5])
    ], 
    remainder='passthrough'
)

X_train_dummy = preprocesser.fit_transform(X_train)
X_test_dummy = preprocesser.transform(X_test)

# Train model
dtr = DecisionTreeRegressor()
dtr.fit(X_train_dummy, y_train)

# Evaluate
y_pred = dtr.predict(X_test_dummy)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Training Complete!")
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.4f}")

# Save models
os.makedirs('app/ml_models', exist_ok=True)
pickle.dump(dtr, open("app/ml_models/dtr.pkl", "wb"))
pickle.dump(preprocesser, open("app/ml_models/preprocesser.pkl", "wb"))

print("Models saved to app/ml_models/")
