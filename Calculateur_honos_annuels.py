import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fonction pour calculer les honoraires
def calcul_honoraires_grille(investissement, paliers):
    fees = 0
    for min_, max_, fixe, taux in paliers:
        if investissement > min_:
            tranche = min(investissement, max_) - min_
            fees += fixe + taux * tranche
        else:
            break
    return fees

st.title('Calculateur d\'Honoraires Publicitaires')

# Paramétrage des paliers d'investissement avec tableau
st.sidebar.header('Paramétrage des Paliers')
num_paliers = st.sidebar.slider("Nombre de paliers", min_value=4, max_value=8, value=4)

data = {'Investissement Max': [], 'Montant Fixe': [], 'Taux': []}
previous_max = 0.0

for i in range(num_paliers):
    st.sidebar.markdown(f"### Palier {i + 1}")
    max_investissement = st.sidebar.number_input(
        f"Investissement maximum pour le palier {i + 1}",
        min_value=previous_max + 0.01, step=1000.0,
        value=previous_max + 1000.0
    )
    fixe = st.sidebar.number_input(f"Montant fixe pour le palier {i + 1}", min_value=0.0, step=1000.0)
    taux = st.sidebar.number_input(f"Taux pour le palier {i + 1}", min_value=0.000, step=0.005, format="%.3f")
    data['Investissement Max'].append(max_investissement)
    data['Montant Fixe'].append(fixe)
    data['Taux'].append(taux)
    previous_max = max_investissement

paliers = [(0.0, data['Investissement Max'][0], data['Montant Fixe'][0], data['Taux'][0])]
for i in range(1, num_paliers):
    paliers.append((data['Investissement Max'][i - 1], data['Investissement Max'][i], data['Montant Fixe'][i], data['Taux'][i]))

df = pd.DataFrame(data)
st.sidebar.write("Résumé des Paliers :")
st.sidebar.table(df)

# Saisie des montants d'investissement mensuels
st.header('Saisie des Montants d\'Investissement Mensuels')
investissement_mensuel = {}
for month in range(1, 13):
    investissement_mensuel[month] = st.number_input(f"Investissement pour le mois {month}", min_value=0.0, step=1000.0, value=0.0)

# Calcul du total annuel des honoraires et du pourcentage de l'investissement
total_honoraires_annuels = sum(calcul_honoraires_grille(inv, paliers) for inv in investissement_mensuel.values())
total_investissement_annuel = sum(investissement_mensuel.values())
pourcentage_honoraires = (total_honoraires_annuels / total_investissement_annuel * 100) if total_investissement_annuel else 0

st.header('CA et taux annuel moyen en fonction de la grille')
st.write(f"**Montant total des honoraires annuels :** {total_honoraires_annuels:.2f} €")
st.write(f"**Pourcentage de l'investissement annuel :** {pourcentage_honoraires:.2f} %")

st.header('CA et taux mensuel en fonction du niveau d\'investissement')

#graphe projection mensuelle
investissements = np.arange(20000, 200000, 1000)
montants_honoraires = [calcul_honoraires_grille(i, paliers) for i in investissements]
pourcentages_honoraires = [calcul_honoraires_grille(i, paliers) / i * 100 for i in investissements]

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Investissements publicitaires (€)')
ax1.set_ylabel('Montant honoraires (€)', color=color)
line1 = ax1.plot(investissements, montants_honoraires, color=color, label='Montant honoraires')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Pourcentage honoraires (%)', color=color)
line2 = ax2.plot(investissements, pourcentages_honoraires, color=color, label='% honoraires')
ax2.tick_params(axis='y', labelcolor=color)

ax1.grid(True, linestyle='--', alpha=0.7)
ax2.grid(True, linestyle=':', alpha=0.7)

# Ajouter les annotations tous les 20 000 €
step = 25000
for inv, mont, perc in zip(investissements, montants_honoraires, pourcentages_honoraires):
    if inv % step == 0:
        # Pour montants
        ax1.annotate(f'{mont:.0f}€', 
                     xy=(inv, mont), 
                     xytext=(0, 10), 
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='blue'),
                     fontsize=8, fontweight='bold', 
                     color='blue')

        # Pour pourcentages
        ax2.annotate(f'{perc:.1f}%', 
                     xy=(inv, perc), 
                     xytext=(0, -15), 
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='red'),
                     fontsize=8, fontweight='bold', 
                     color='red')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

plt.title('Grille dégressive des honoraires', pad=20, fontsize=14)
plt.tight_layout()

st.pyplot(fig)

