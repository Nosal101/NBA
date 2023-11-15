# -*- coding: utf-8 -*-
"""Zawodnicy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JIBMqXwaRPHtDBHS6R5I9zU4dF7xl8d7

Cechy jakie chcemy zbadać:
- Porównać zawodników w każdej z kategori ✅
- Pogrupować zawodników na ich klasy (wybitnych i mniej wybitnych) ✅
- Znaleźć zawodników najleprzych na swoich pozycjach
- Znaleźć najlepszy wiek dla gracza
- Wyznaczyć statystyki które definiują gracza (chce wywalić zbędne statystyki by nie używać ich w dalszych analizach) ✅
- Sprawdzić jakie statystyki musi mieć gracz by być w topce
- Znaleźć mocne i słabe strony kazdej z drużyn
- Zrobić wykresy korelacyjne ✅

#Przygotownie danych do analizy

##Importownie Bibliotek
"""

# Commented out IPython magic to ensure Python compatibility.
# %reset -f
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""##Wczytanie Danych"""

dataset1 = pd.read_csv('Statystyki_zawodników.csv', encoding='latin-1');
#Rk - nr zawodnika #nie uzyte
#Player - Imie zawodnika
#Pos - Pozycja na boisku
#Age = Wiek gracz
#Tm - Drużyna
#G - Rozegrane mecze
#GS - Rozegrane mecze w pierwszym składzie
#MP - Minuty na mecz
#FG - Liczba trafionych rzutów z gry na mecz
#FGA - Liczba prób rzutów na mecz
#FG% - Procent trafionych rzutów
#3P - Liczba trafionych rzutów za 3
#3PA - Liczba prób za 3 na mecz
#3P% - Procent trafionych rzutów za 3
#2P - Liczba trafionych rzutów za 2
#2PA - Liczba prób za 2 na mecz
#2P% - Procent trafionych rzutów za 2
#eFG% - Procent efektywnych rzutów
#FT - Liczba trafionych osobistych na mecz
#FTA - Liczba prób z osobistych na mecz
#FT% - Procent trafionych rzutów osobistych
#ORB - Ofensywne zbiórki na mecz
#DRB - Defensywne zbiórki na meczz
#TRB - Całkowita suma zbiórek na mecz
#AST - Astsy na mecz
#STL - Przechwyty na mecz
#BLK - Bloki na mecz
#TOV - Straty na mecz
#PF - Faule na mecz
#PTS - Punkty na mecz
#Player-assitional - nie wiem w sumie co to #nie użyte
dataset2 = pd.read_csv('Statystyki_zawodników_rzuty.csv', encoding='latin-1');
#Rk - nr zawodnika #nie uzyte
#Player - Imie zawodnika #nie uzyte
#Pos - Pozycja na boisku #nie uzyte
#Age = Wiek gracz #nie uzyte
#Tm - Drużyna #nie uzyte
#G - Rozegrane mecze #nie uzyte
#MP - Minuty na mecz #nie uzyte
#FG% - Procent trafionych rzutów #nie uzyte
#Dist - Średni dystans odległości oddawanych rzutów
#2P - Procent liczba prób rzutów za 2
#0-3 - Procent próby z odległości 0-3 stóp
#3-10 - Procent próby z odległości 3-10 stóp
#10-16 - Procent próby z odległości 10-16 stóp
#16-3P - Procent próby z odległości 16-3P stóp
#3P -  Procent liczby prób rzutów za 3
#2P - Procent liczby trafionych rzutów za 2
#0-3 - Procent trafionyhch z odległości 0-3 stóp
#3-10 - Procent trafionych z odległości 3-10 stóp
#10-16 - Procent trafionych z odległości 10-16 stóp
#16-3P -  Procent trafionych z odległości 16-3P stóp
#3P - Procent trafionych rzutów za 3
#2P - Procent punktów za 2 po asyście
#3P - Procent punktów za 3 po asyście
#%FGA - Procent danków w próbach rzutów
## - liczba danków
#%3PA - Procent prób rzutów za 3 wykonanych z narożnika
#%3P - Procent trafionych rzutów za 3 wykonanych z narożnika
#Ostatnie 3 to nie wiem co to #nie użyte

"""##Połącznie zbiorów i wstępne ich przygotowanie"""

data1 = dataset1.iloc[:, [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]]

data2 = dataset2.iloc[:, [8,10,11,12,13,14,15,17,18,19,20,21,22,24,25,27,28,30,31]]

Stat_zawodnikow = pd.concat([data1,data2],axis=1)

print(dataset1.shape)
print(dataset2.shape)
print(data1.shape)
print(data2.shape)

print(Stat_zawodnikow.shape)

"""Okej trzeba sie zastanowić co zrobić z zawodnikami którzy zmienili klub w trakcie sezonu bo niektóre statystyki sie dodają do siebie jak np mecze ale średnie ale niektóre dane dą procentowe wiec trzeba je liczyć średnią i co zrobić z brakującymi danymi"""

# Wpisanie w każydum polu nan 0
Stat_zawodnikow = Stat_zawodnikow.fillna(0)

"""Postanowiłem poprostu usunąć zawodników którzy sie powtarzają i zostawić tylko tego w najbardziej aktualnym klubie"""

# Znalezienie indeksów zawodników zduplikowanych
duplicated_indices = Stat_zawodnikow[Stat_zawodnikow.duplicated(['Player'])].index

# Usunięcie wszystkich duplikatów oprócz pierwszego wystąpienia
Stat_zawodnikow.drop(duplicated_indices, inplace=True)

print(Stat_zawodnikow.shape)

"""Dane są super przygotowane do obróbki

#Usunięcie kolumn nie noszących cennych danych
"""

print(Stat_zawodnikow.dtypes)

"""##Progowanie wariancji cechy liczbowej"""

from sklearn.feature_selection import VarianceThreshold

X_data = Stat_zawodnikow.iloc[:,4:]

tresh = VarianceThreshold(threshold=0.5)
tresh.fit_transform(X_data)

mask = tresh.get_support()
indexes_of_tresh = np.where(mask)[0]

index_of_important_data = []
for i in range(4):
  index_of_important_data.append(i)

for i in indexes_of_tresh:
  index_of_important_data.append(i+4)

Data_to_analysis = Stat_zawodnikow.iloc[:,index_of_important_data]
print(Data_to_analysis)

"""#Analiza Korelacji statystyk"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
Correlation_Data = sc.fit_transform(Data_to_analysis.iloc[:,[i for i in range(len(Data_to_analysis.columns)) if i not in [0, 1, 3]]])
Correlation_Data = pd.DataFrame(Correlation_Data, columns=[Data_to_analysis.columns[i] for i in range(len(Data_to_analysis.columns)) if i not in [0, 1, 3]])
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(Correlation_Data.corr(),vmin=-1, vmax=1, annot=True);
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);

"""Wnioski :

Nie bede opisuwał jakiś logicznych korelcji np miedzy próbami za 3 a trafionymi rzutami za 3 jak i rozegranymi meczami i minutami na boisku skupie sie na mniej oczywisty

Występuje mocna korelacja miedzy wyjściem w pierwszym składzie a zdobywanymi pkt i minutami spedzonymi na boisku co świadcy o tym że zawodnicy w pierwszym składzie stanowią o sile drużyny.

Cekawe jest wystąpienie silnej korelacji miedzy trafionymi rzutami do kosza a stratami jak i zbiórkami w defensywie

Taka sama koleracja wystepuje w rzutach za 2 a stratami i zbiórkami w defensywie

Występuje też silna korelacja miedzy zbiórkami ofensywnymi a wsadami co wynika z tego że czesto zawodnicy po zbiurce kończą akcje wsadem

Istnieje też zależność miedzy zbiórkami a faluami zawodników co wynika z ostrej gry zawodników odpowiedzialnych za defensywne zbiurki

Występuje silna korelacja miedzy asystami a stratami co moze wynikać z tego ze podczas wielu podań piłka morze zostać przechwycowa oraz zdobywanymi punktami
co świadczy że zawodnicy którzy dużo podają czesto nie mając opcji na podanie decydują sie na rzuty i tym samym na pkt

#Grupowanie

##Grupowanie zawodników za pomocą K-Means
"""

from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import StandardScaler

Data_to_analysis_copy = Data_to_analysis.copy()

X = Data_to_analysis.iloc[:, 7:].values

sc = StandardScaler()
X = sc.fit_transform(X)

model = KMeans()
visualizer = KElbowVisualizer(model, k=(1,12), timings=False)

visualizer.fit(X)
visualizer.show()

kmeans = KMeans(n_clusters=4, random_state=0, init="k-means++")
y_kmeans = kmeans.fit_predict(X)

index_0 = [index for index,value in enumerate(y_kmeans) if value == 0]
index_1 = [index for index,value in enumerate(y_kmeans) if value == 1]
index_2 = [index for index,value in enumerate(y_kmeans) if value == 2]
index_3 = [index for index,value in enumerate(y_kmeans) if value == 3]

#Dodaje do wykresu informacje o liczbie gier, gier w pierwszej drużynie i liczbie minut na mecz
#Lecz nie uwzględniam ich w modelu ponieważ nie są to statystyki wypracowane przez zawodnika a decyzja trenera
X_new = Data_to_analysis.iloc[:, [i for i in range(len(Data_to_analysis.columns)) if i not in [0, 1, 3]]].values
sc_new = StandardScaler()
X_new = sc.fit_transform(X_new)

Data_to_analysis_copy.iloc[:, 7:] = X

Data_to_analysis_copy['GA'] = X_new[:,1] #GAMES
Data_to_analysis_copy['GAS'] = X_new[:,2] #GAMES IN FIRST TEAM
Data_to_analysis_copy['GAM'] = X_new[:,3] #MINUTES PER GAME


mean_index_0 = Data_to_analysis_copy.iloc[index_0,7:].mean()
mean_index_1 = Data_to_analysis_copy.iloc[index_1,7:].mean()
mean_index_2 = Data_to_analysis_copy.iloc[index_2,7:].mean()
mean_index_3 = Data_to_analysis_copy.iloc[index_3,7:].mean()

# Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.plot(mean_index_0.index, mean_index_0.values, marker='o', linestyle='-', color='b', label='Grupa 1')
plt.plot(mean_index_1.index, mean_index_1.values, marker='o', linestyle='-', color='g', label='Grupa 2')
plt.plot(mean_index_2.index, mean_index_2.values, marker='o', linestyle='-', color='r', label='Grupa 3')
plt.plot(mean_index_3.index, mean_index_3.values, marker='o', linestyle='-', color='c', label='Grupa 4')
plt.xlabel('Statystyki')
plt.ylabel('Średnie po standaryzacji')
plt.title('Wykres średnich dla każdej kolumny')
plt.legend()
plt.show()

"""WNIOSKI:

Algorytm podzielił zawodników na 4 grupy:

Grupa1 to zawodnicy słabi rezerwowi co pokazują ich statystyki które śa poniżej średniej praktycznie w każdej kategori

Grupa2 to zawodnicy najlepsi gwiazdy swoich drużyn grają nawiecej i zdobywają najlepsze statystki

Grupa3 to zawodnicy rzucający za 3, asystujący

Grupa4 to zawodnicy grający blisko kosza, mający wiele zbiurek, fauli i wsadów

Owe grupy zawodników przydadzą sie po analizie drużyn w jakich miejscach odstają i w jakiej grupie zawodników powinni szukać przyszłych transwerów

# Analiza cech kazdej z pozycji

##Podział zawodników na odpowiadające im pozycje
"""

Data_to_posision = Data_to_analysis.copy()

Data_to_posision = Data_to_posision[(Data_to_posision.iloc[:, 5] != 0) & (Data_to_posision.iloc[:, 4] >= 10)]

X_n = Data_to_posision.iloc[:, 4:].values
sc_n = StandardScaler()
X_n = sc.fit_transform(X_n)

Data_to_posision.iloc[:,4:] = X_n

pos_C = []
pos_PF = []
pos_PG = []
pos_SF = []
pos_SG = []
for i in range(len(Data_to_posision)):
  #Zawodnicy o jednej pozycji
    if Data_to_posision.iloc[i, 1] == 'C':
        pos_C.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'PF':
        pos_PF.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'PG':
        pos_PG.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SF':
        pos_SF.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SG':
        pos_SG.append(Data_to_posision.iloc[i, :])
  #Zawodnicy o dwóch pozycji
    if Data_to_posision.iloc[i, 1] == 'PF-C':
        pos_PF.append(Data_to_posision.iloc[i, :])
        pos_C.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'PF-SF':
        pos_PF.append(Data_to_posision.iloc[i, :])
        pos_SF.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'PG-SG':
        pos_PG.append(Data_to_posision.iloc[i, :])
        pos_SG.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SF-PF':
        pos_SF.append(Data_to_posision.iloc[i, :])
        pos_PF.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SF-SG':
        pos_SF.append(Data_to_posision.iloc[i, :])
        pos_SG.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SG-PG':
        pos_SG.append(Data_to_posision.iloc[i, :])
        pos_PG.append(Data_to_posision.iloc[i, :])

pos_C = pd.DataFrame(pos_C)
pos_PF = pd.DataFrame(pos_PF)
pos_SG = pd.DataFrame(pos_SG)
pos_PG = pd.DataFrame(pos_PG)
pos_SF = pd.DataFrame(pos_SF)

plt.figure(figsize=(10, 6))
plt.plot(pos_C.iloc[:,4:].mean(axis = 0), marker='o',color = 'b',label = 'C')
plt.plot(pos_PF.iloc[:,4:].mean(axis = 0), marker='o',color = 'r',label = 'PF')
plt.plot(pos_SG.iloc[:,4:].mean(axis = 0), marker='o',color = 'g',label = 'SG')
plt.plot(pos_PG.iloc[:,4:].mean(axis = 0), marker='o',color = 'm',label = 'PG')
plt.plot(pos_SF.iloc[:,4:].mean(axis = 0), marker='o',color = 'c',label = 'SF')
plt.xlabel('Statystyki')
plt.ylabel('Średnie po standaryzacji')
plt.title('Wykres średnich dla każdej pozycji')
plt.legend()
plt.show()

"""Wnioski :

C(center) - Zawodnik opowiedzialny za zbiórki, faule i wsady

PF(Silny Skrzydłowy) - Bardzo równy we wszytkim widoczne skłonności w statystykach gdzie dominuje Center

SG(Rzucający Obrońca) - Głównie rzucają za 3

PG(Rozgrywający) - Oddaje najwiecej rzutów na boisku co przekłada sie na najwiekszą liczbę punktów na mecz, głównie odpowiedzialni za rozdawanie asyst

SF(Niski skrzydłowy) - Statystyki podobne do SG lecz posiada wiecej zbiórek

#Predykcja Pozycji na bazie Statystyk

##Przygotowanie Danych
"""

pos_C = []
pos_PF = []
pos_PG = []
pos_SF = []
pos_SG = []
for i in range(len(Data_to_posision)):
  #Zawodnicy o jednej pozycji
    if Data_to_posision.iloc[i, 1] == 'C':
        pos_C.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'PF':
        pos_PF.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'PG':
        pos_PG.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SF':
        pos_SF.append(Data_to_posision.iloc[i, :])
    if Data_to_posision.iloc[i, 1] == 'SG':
        pos_SG.append(Data_to_posision.iloc[i, :])

pos_C = pd.DataFrame(pos_C)
pos_PF = pd.DataFrame(pos_PF)
pos_SG = pd.DataFrame(pos_SG)
pos_PG = pd.DataFrame(pos_PG)
pos_SF = pd.DataFrame(pos_SF)

all_pos = pd.concat([pos_C, pos_PF, pos_PG, pos_SF,pos_SG], ignore_index=True)
X = all_pos.iloc[:, 4:].values
y = all_pos.iloc[:, 1].values

print(all_pos)

from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
y = encoder.fit_transform(y.reshape(-1, 1)).toarray()
print(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

"""## Build ANN"""

import tensorflow as tf
ann = tf.keras.models.Sequential()

ann.add(tf.keras.layers.Dense(5,activation='relu'))
ann.add(tf.keras.layers.Dense(32,activation='relu'))
ann.add(tf.keras.layers.Dense(64,activation='relu'))
ann.add(tf.keras.layers.Dense(128,activation='relu'))
ann.add(tf.keras.layers.Dense(256,activation='relu'))
ann.add(tf.keras.layers.Dense(5,activation='softmax'))
ann.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics=['accuracy'])

ann.fit(X_train, y_train ,epochs = 300)

y_pred = ann.predict(X_test)

y_test_numeric = np.argmax(y_test, axis=1)
y_pred_numeric = np.argmax(y_pred, axis=1)
print(y_test_numeric)

print(y_pred_numeric)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test_numeric, y_pred_numeric)
print(cm)
accuracy_score(y_test_numeric, y_pred_numeric)

# 0 - C
# 1- PF
# 2 - PG
# 3 - SF
# 4 - SG

"""Wnioski :

Jesteśmy bardzo dobrze przewidzieć pozycje jeżeli zawodnik gra na pozycji C i PG co pokazywał wykres średnich statystyk dla każdej z pozycji
"""