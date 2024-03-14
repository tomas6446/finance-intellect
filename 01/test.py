import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dates = pd.date_range('20190214', periods=6)
numbers = np.matrix([[101, 103], [105.5, 75], [102, 80.3], [100, 85], [110, 98], [109.6, 125.7]])
df = pd.DataFrame(numbers, index=dates, columns=['A', 'B'])

print('1. gauti eilutę, kurios indekso data yra stringas 2019-02-18')
eilute = df.loc['2019-02-18']
print(eilute)

print('\n2. gauti eilutę, kurios indekso data yra datetime.datetime (2019,2,18)')
date_datetime = datetime.datetime(2019, 2, 18)
row_datetime = df.loc[date_datetime]
print(row_datetime)

print('\n3. gauti eilutę, kuri yra priešpaskutinė nuo galo (nenaudoti indekso)')
nuogalo = df.iloc[-2]
print(nuogalo)

print('\n4. gauti pirmas 2 eilutes ir stulpeli B (nenaudoti indekso)')
first_two_rows_b_corrected = df.iloc[:2]['B']
print(first_two_rows_b_corrected)

print('\n5. Išrūšiuoti df pagal B stulpelį mažėjančia tvarka')
df_sorted_by_b = df.sort_values(by='B', ascending=False)
print(df_sorted_by_b)

print('\n6. Rasti stulpelio A didžiausią reikšmę')
max_value_a = df['A'].max()
print(max_value_a)

print('\n7. Padvigubinti stulpelio A didžiausią reikšmę')
df.loc[df['A'] == max_value_a, 'A'] = max_value_a * 2  # selects the row where A is max and sets A to max * 2
df_sorted_by_b = df.sort_values(by='B', ascending=False)
print(df_sorted_by_b)

print('\n8. Gauti eilutes, kur stulpelio A reikšmės didesnės už 105')
rows_greater_than_105 = df[df['A'] > 105]
print(rows_greater_than_105)

print("\n9. Nupiesti plot stupelio A reiksmes")
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['A'], marker='o', linestyle='-', color='blue')
plt.title('Stulpelio "A" reikšmių grafikas')
plt.xlabel('Data')
plt.ylabel('Reikšmės')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n10. istrinti eilutes, kur stupelio B reiksmes yra didesnes uz stulpelio A reiksmes")
df_filtered = df[df['B'] <= df['A']]
df_sorted_by_b = df_filtered.sort_values(by='B', ascending=False)
print(df_sorted_by_b)

print("\n1. Suma 2 vektoriu")
a = np.random.randint(low=1, high=10, size=10)
b = np.random.randint(low=1, high=10, size=10)
c = a + b
print(c)

print("\n2. Anuliavimas teigiamų elementų")
a = np.random.randint(low=-10, high=10, size=10)
a[a > 0] = 0
print(a)

print("\n3. Išmetimas > 6")
a = np.random.randint(low=1, high=10, size=10)
b = a[a <= 6]
print(a)
print(b)

print("\n4. Dviejų vienodų šalia esančių radimas")
a = np.random.randint(1, 6, size=10)
print(f"a = {a}")
for i in range(1, len(a)):
    if a[i] == a[i - 1]:
        print(i)

print("\n5. Elementų, kur a elementai didesni už b elementus, radimas")
a = np.random.randn(10)
b = np.random.randn(10)
for i in range(len(a)):
    if a[i] > b[i]:
        print(i)

print("\n6. Elementų perstūmimas vektoriuje, pakartojant paskutinį")
a = np.random.randint(1, 11, size=10)
print(a)
for i in range(1, len(a)):
    a[i - 1] = a[i]
print(a)

print("\n7. Sukeitimas elementų eilės tvarkos")
a = np.random.randint(1, 11, size=10)
print(a)
for i in range(len(a) // 2):
    b = a[i]
    a[i] = a[len(a) - i - 1]
    a[len(a) - i - 1] = b
print(a)

print("\n8. Kas antro elemento užnulinimas")
a = np.random.randint(1, 11, size=10)
print(a)
for i in range(0, len(a), 2):
    a[i] = 0
print(a)

print("\n9. Rasti matricos eilučių vidurkius, rasti matricos stulpelių vidurkius")
a = np.random.randn(10, 20)
# Eilučių vidurkiai
print("Eilučių vidurkiai:")
for i in range(a.shape[0]):
    print(np.mean(a[i, :]))

# Stulpelių vidurkiai
print("Stulpelių vidurkiai:")
for j in range(a.shape[1]):
    print(np.mean(a[:, j]))

print("\n10. Gauti matricos diagonalinius elementus (be diag funkcijos)")
a = np.random.randint(1, 11, size=(10, 10))
for i in range(a.shape[0]):
    print(a[i, i])
