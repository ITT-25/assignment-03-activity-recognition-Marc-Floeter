# this program recognizes activities

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Parameter
DATA_DIR = 'data'
WINDOW_SIZE = 100  # 1 Sekunde bei 100Hz
STEP_SIZE = 100

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"]
COLUMNS = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]

X = []
y = []

def main():
    X, y = load_data()

    print("X shape:", X.shape)
    print("y shape:", y.shape)
    print("Beispiel-Feature-Vektor:", X[0])
    print("Label dazu:", y[0])

########################################################################################################################################################################################
# DATEN LADEN UND PREPROCESSING
########################################################################################################################################################################################

def load_data():
    X = []
    y = []

    for activity in ACTIVITIES:
        activity_dir = os.path.join(DATA_DIR, activity)

        if not os.path.isdir(activity_dir):
            continue

        for filename in os.listdir(activity_dir):
            if not filename.endswith('.csv'):
                continue

            filepath = os.path.join(activity_dir, filename)
            try:
                print(f"Lade Datei: {filepath}")
                df = pd.read_csv(filepath)
                df[COLUMNS] = df[COLUMNS].fillna(method='ffill') # Leere Werte mit dem Wert der vorherigen Zeile auffüllen
                df[COLUMNS] = df[COLUMNS].fillna(0) # Falls am Anfang der Datei noch NaNs sind (weil kein vorheriger Wert)

            except pd.errors.ParserError as e:
                print(f"Fehler beim Einlesen von {filepath}: {e}")
                continue  # Datei überspringen

            # Gleitende Fenster
            for start in range(0, len(df) - WINDOW_SIZE + 1, STEP_SIZE):
                window = df.iloc[start:start+WINDOW_SIZE]
                features = extract_features(window)
                X.append(features)
                y.append(activity)

    return np.array(X), np.array(y)


def extract_features(window):
    features = []
    for axis in COLUMNS:
        data = window[axis]
        features += [
            data.mean(),
            data.std(),
            data.max(),
            data.min()
        ]
    return features

def split_train_test_data():
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

def normalize_data():
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

if __name__ == "__main__":
    main() 