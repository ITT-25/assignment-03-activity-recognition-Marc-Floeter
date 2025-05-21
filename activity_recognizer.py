# this program recognizes activities

import os
import pandas as pd
import numpy as np
import pickle
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, confusion_matrix
import dippid_reciever as dr

DATA_DIR = "data"
SAMPLE_RATE = 0.01 # 100Hz
WINDOW_SIZE = 100  # 1 Sekunde bei 100Hz
STEP_SIZE = 100 # Keine Überlappung der Fenster
PREDICTION_RATE = 0.1 # 10Hz 
KERNEL = "poly"

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"]
COLUMNS = ["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"]

features = []
classes = []
features_train = []
classes_train = []
features_test = []
classes_test = []

standard_scaler = None
minmax_scaler = None
classifier = None

loading = True

def main():
    global loading
    
    load_data()
    preprocess_data()
    train_classifier()
    evaluate_classifier()
    loading = False
    live_prediction()


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
                window_features = extract_features_training_data(window)
                features.append(window_features)
                classes.append(ACTIVITIES.index(activity)) # Benutzt als numerische Klasse gleich die position der Aktivität in der Aktivitätenliste

    features = np.array(features)
    classes = np.array(classes)


def extract_features_training_data(window):
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
    global standard_scaler, features_train, features_test

    print("Featuredaten standardisieren")
    standard_scaler = StandardScaler()
    standard_scaler.fit(features_train)
    features_train = standard_scaler.transform(features_train)
    features_test = standard_scaler.transform(features_test)


def normalize_feature_data():
    global minmax_scaler, features_train, features_test

    print("Featuredaten normalisieren")
    minmax_scaler = MinMaxScaler()
    minmax_scaler.fit(features_train) # Scaler orientiert sich nur an den Trainingsdaten (Testdaten sollen ja keinen Einfluss haben)
    features_train = minmax_scaler.transform(features_train)
    features_test = minmax_scaler.transform(features_test)


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
# LIVE PREDICTION
##########################################################################################

def live_prediction():
    print("Starte Live-Erkennung...")
    while True:
        if dr.training:
            time.sleep(PREDICTION_RATE)
            features_live = extract_features_live_data()
            if features: # Also eigentlich: falls genügend Daten im Buffer gesammelt waren
                standardized_features_live = standard_scaler.transform([features_live])
                normalized_features_live = minmax_scaler.transform([standardized_features_live])
                prediction = model.predict(normalize_features_live)[0]
                print(f"Aktuelle Aktivität: {prediction}")
            else:
                print("Nicht genügend Daten im Buffer")
        else:
            print("Warte auf Start des Trainings per dippid")
            time.sleep(PREDICTION_RATE)


def extract_features_live_data():
    features = []
    for buffer in [dr.acc_x, dr.acc_y, dr.acc_z, dr.gyro_x, dr.gyro_y, dr.gyro_z]:
        if len(buffer) < 100:
            return None  # Noch nicht genug Daten
        buffer_array = np.array(buffer)
        features += [
            np.mean(buffer_array),
            np.std(buffer_array),
            np.min(buffer_array),
            np.max(buffer_array)
        ]
    return features

##########################################################################################
if __name__ == "__main__":
    main() 