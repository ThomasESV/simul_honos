import streamlit as st

# Fonction pour calculer les honoraires
def calcul_honoraires_grille(investissement, paliers):
    fees = 0
    for min_, max_, fixe, taux in paliers:
        if investissement > min_:
            tranche = min(investissement, max_) - min_
            fees += fixe + taux * tranche
    return fees

st.title('Calculateur d\'Honoraires Publicitaires')

# Paramétrage des paliers d'investissement
st.sidebar.header('Paramétrage des Paliers')
num_paliers = st.sidebar.slider("Nombre de paliers", min_value=4, max_value=8, value=4)

paliers = []
previous_max = 0.0  # Start with float
for i in range(num_paliers):
    st.sidebar.markdown(f"### Palier {i + 1}")
    max_investissement = st.sidebar.number_input(
        f"Investissement maximum pour le palier {i + 1}",
        min_value=previous_max,
        step=100.0,
        value=previous_max + 100.0  # Set default value appropriately
    )
    fixe = st.sidebar.number_input(f"Montant fixe pour le palier {i + 1}", min_value=0.0, step=10.0)
    taux = st.sidebar.number_input(f"Taux pour le palier {i + 1}", min_value=0.0, step=0.05)
    paliers.append((previous_max, max_investissement, fixe, taux))
    previous_max = max_investissement

# Saisie des montants d'investissement mensuels
st.header('Saisie des Montants d\'Investissement Mensuels')
investissement_mensuel = {}
for month in range(1, 13):
    investissement_mensuel[month] = st.number_input(f"Investissement pour le mois {month}", min_value=0.0, step=100.0, value=0.0)

# Calcul du total annuel des honoraires et du pourcentage de l'investissement
total_honoraires_annuels = sum(calcul_honoraires_grille(inv, paliers) for inv in investissement_mensuel.values())
total_investissement_annuel = sum(investissement_mensuel.values())
pourcentage_honoraires = (total_honoraires_annuels / total_investissement_annuel * 100) if total_investissement_annuel else 0

st.write(f"**Montant total des honoraires annuels :** {total_honoraires_annuels:.2f} €")
st.write(f"**Pourcentage de l'investissement annuel :** {pourcentage_honoraires:.2f} %")
