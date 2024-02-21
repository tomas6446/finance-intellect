import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# a = np.random.random(100)
#
# plt.plot(a)
# plt.title('Akciju linija')
# plt.xlabel('Kaina')
# plt.ylabel('Linija')
# plt.plot(a, color='red')
# plt.show()

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
nuogalo = df.loc['2019-02-18']
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
df.loc[df['A'] == max_value_a, 'A'] = max_value_a * 2
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

