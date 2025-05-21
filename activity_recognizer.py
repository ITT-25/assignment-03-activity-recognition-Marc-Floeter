# this program recognizes activities

import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, confusion_matrix

DATA_DIR = "data"
WINDOW_SIZE = 100  # 1 Sekunde bei 100Hz
STEP_SIZE = 100
KERNEL = "poly"

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"]
COLUMNS = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]

features = []
classes = []

features_train = []
classes_train = []

features_test = []
classes_test = []

classifier = None

def main():
    load_data()
    preprocess_data()
    train_classifier()
    evaluate_classifier()


########################################################################################################################################################################################
# DATEN LADEN UND PREPROCESSING
########################################################################################################################################################################################

def load_data():
    global features, classes

    print("Load Data")
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
                df[COLUMNS] = df[COLUMNS].ffill() # Leere Werte mit dem Wert der vorherigen Zeile auffüllen
                df[COLUMNS] = df[COLUMNS].fillna(0) # Falls am Anfang der Datei noch NaNs sind (weil kein vorheriger Wert)

            except pd.errors.ParserError as e:
                print(f"Fehler beim Laden von {filepath}: {e}")
                continue  # Datei überspringen

            # Gleitende Fenster
            for start in range(0, len(df) - WINDOW_SIZE + 1, STEP_SIZE):
                window = df.iloc[start:start+WINDOW_SIZE]
                window_features = extract_features(window)
                features.append(window_features)
                classes.append(ACTIVITIES.index(activity)) # Benutzt als numerische Klasse gleich die position der Aktivität in der Aktivitätenliste

    features = np.array(features)
    classes = np.array(classes)

    # print("X Aufbau:", X.shape)
    # print("y Aufbau:", y.shape)
    # print("Features", X[0])
    # print("Label dazu:", y[0])


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


def preprocess_data():
    split_train_test_data()
    standardize_feature_data()
    normalize_feature_data()


def split_train_test_data():
    global features_train, features_test, classes_train, classes_test

    print("Daten in Training (80%) und Test Data (20%) aufteilen")
    features_train, features_test, classes_train, classes_test = train_test_split(
        features, classes, test_size=0.2, random_state=42, stratify=classes
    )


def standardize_feature_data():
    global features_train, features_test

    print("Featuredaten standardisieren")
    scaler = StandardScaler()
    scaler.fit(features_train)
    features_train = scaler.transform(features_train)
    features_test = scaler.transform(features_test)


def normalize_feature_data():
    global features_train, features_test

    print("Featuredaten normalisieren")
    scaler = MinMaxScaler()
    scaler.fit(features_train) # Scaler orientiert sich nur an den Trainingsdaten (Testdaten sollen ja keinen Einfluss haben)
    features_train = scaler.transform(features_train)
    features_test = scaler.transform(features_test)


##########################################################################################
# CLASSIFIER TRAINIEREN UND EVALUIEREN
##########################################################################################

def train_classifier():
    global classifier

    print("Classifier (SVC) mit Trainingsdaten trainieren")
    classifier = svm.SVC(kernel = KERNEL)
    classifier.fit(features_train, classes_train)


def evaluate_classifier():
    classes_predicted = classifier.predict(features_test)
    print("Accuracy:", accuracy_score(classes_test, classes_predicted))

    conf_matrix = confusion_matrix(classes_test, classes_predicted)
    ConfusionMatrixDisplay(conf_matrix, display_labels=ACTIVITIES).plot()
    plt.xticks(rotation=90)
    plt.show()

##########################################################################################
if __name__ == "__main__":
    main() 