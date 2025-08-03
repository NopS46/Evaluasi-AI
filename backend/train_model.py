import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Buat data dummy (100 siswa)
np.random.seed(42)
data = {
    'projectComplexity': np.random.randint(1, 11, 100),
    'solutionInnovation': np.random.randint(1, 11, 100),
    'implementationQuality': np.random.randint(1, 11, 100),
    'debuggingAbility': np.random.randint(1, 11, 100),
    'presentationScore': np.random.randint(1, 11, 100)
}

# Asumsikan nilai kreativitas dan problem solving adalah gabungan beberapa faktor
df = pd.DataFrame(data)
df['creativityScore'] = (
    0.4 * df['solutionInnovation'] +
    0.3 * df['presentationScore'] +
    0.3 * df['projectComplexity']
) + np.random.normal(0, 1, 100)

df['problemSolvingScore'] = (
    0.5 * df['debuggingAbility'] +
    0.3 * df['implementationQuality'] +
    0.2 * df['projectComplexity']
) + np.random.normal(0, 1, 100)

# Fitur dan target
X = df[['projectComplexity', 'solutionInnovation', 'implementationQuality', 'debuggingAbility', 'presentationScore']]
y1 = df['creativityScore']
y2 = df['problemSolvingScore']

# Model 1: Kreativitas
model_creativity = LinearRegression().fit(X, y1)
joblib.dump(model_creativity, 'model_creativity.pkl')

# Model 2: Problem Solving
model_problemsolving = LinearRegression().fit(X, y2)
joblib.dump(model_problemsolving, 'model_problemsolving.pkl')

print("✅ Model regresi telah dibuat dan disimpan sebagai 'model_creativity.pkl' dan 'model_problemsolving.pkl'")
