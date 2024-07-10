import geopandas as gpd
import numpy as np
import pandas as pd
import random
from shapely.geometry import MultiPoint
from IPython.display import display
from sklearn.impute import SimpleImputer

data_acc = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/combain_data/data_acc.gpkg")
data_non_acc = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/combain_data/data_non_acc.gpkg")
print(data_non_acc.shape)

def unify_crs(df1, df2):
    df1.crs = df2.crs
    return df1


def combine_dataframes(df1, df2, reset_index=True):
    combined_df = pd.concat([df1, df2], axis=0)
    if reset_index:
        combined_df.reset_index(drop=True, inplace=True)
    return combined_df

def get_percentage(data):
    missing_percentage = data.isnull().sum() / len(data) * 100
    display(missing_percentage)


data_acc = unify_crs(data_acc, data_non_acc)

combined_data = combine_dataframes(data_acc, data_non_acc)
get_percentage(combined_data)
combined_data = combined_data.drop(columns=["annee_permis", "annee_veh", "index_right","Weekend"])
# Convertir les colonnes de type Timestamp en format de chaîne de caractères
combined_data['Date_Acci'] = combined_data['Date_Acci'].astype(str)
combined_data['date_naissance'] = combined_data['date_naissance'].astype(str)
print(combined_data.info())

# Écrire le DataFrame dans le fichier GeoPackage
#combined_data.to_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/combain_data/combain_data.gpkg")

#Lebel_Encoding
combined_data1 = combined_data.fillna(value=0)
combined_data1['accident'] = combined_data1['type_acc'].apply(lambda x: 1 if x in ['AC', 'AM', 'AMO'] else 0)
combined_data1.drop(['type_acc', 'nbre_dec', 'nbre_bless', 'heure_acc', 'cause_acc', 'Date_Acci', 'Age',
                      'Wilaya', 'Commune', 'date_naissance', 'marque_veh'], axis=1, inplace=True)

def get_features_to_one_hot_encode(df, exclude=None, max_unique_values=50):
    if exclude is None:
        exclude = []
    
    features_to_one_hot_encode = [
        column for column in df.select_dtypes(include=[object]).columns
        if df[column].nunique() <= max_unique_values and column not in exclude
    ]
    
    return features_to_one_hot_encode

def one_hot_encode_columns(df, columns_to_encode, drop_first=True):
    # Comptage initial des features
    feature_count_pre = df.shape[1]
    print("Number of features originally:", feature_count_pre)

    # Afficher les colonnes à encoder
    display(df[columns_to_encode])

    # Encodage one-hot
    df_encoded = pd.get_dummies(df[columns_to_encode], drop_first=drop_first)

    # Concaténer les nouvelles colonnes encodées avec le DataFrame original
    df = pd.concat((df, df_encoded), axis=1)

    # Afficher le nombre de nouvelles features ajoutées
    print("Number of features added:", df.shape[1] - feature_count_pre)

    # Mise à jour du comptage des features après ajout
    feature_count_pre = df.shape[1]

    # Supprimer les colonnes originales encodées
    df = df.drop(columns=columns_to_encode, axis=1)

    # Afficher le nombre de features supprimées
    print("Number of features dropped:", -(df.shape[1] - feature_count_pre))

    return df

def replace_boolean_with_numeric(df):
    # Remplacer les valeurs True par 1 et les valeurs False par 0
    df = df.replace(to_replace=True, value=1)
    df = df.replace(to_replace=False, value=0)
    
    return df




exclude = ['accident']
features_to_one_hot_encode = get_features_to_one_hot_encode(combined_data1, exclude)
# Afficher les colonnes identifiées pour l'encodage one-hot
print(features_to_one_hot_encode)


combined_data1 = one_hot_encode_columns(combined_data1, features_to_one_hot_encode)
# Afficher les premières lignes du DataFrame mis à jour pour vérifier
print(combined_data1.head())


combined_data1 = replace_boolean_with_numeric(combined_data1)
# Afficher les premières lignes du DataFrame mis à jour pour vérifier
print(combined_data1.head())

# prompt: combined_data1 to gpkg
combined_data1.to_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/combain_data/combined_data_encoding.gpkg")