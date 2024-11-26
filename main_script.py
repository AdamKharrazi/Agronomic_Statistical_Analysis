import streamlit as st
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Analyse Statistique pour les Expérimentations Agronomiques : ANOVA et Test de Student")

# Charger le fichier Excel
def charger_fichier():
    fichier = st.file_uploader("Chargez un fichier Excel", type=["xlsx", "xls"])
    if fichier is not None:
        data = pd.read_excel(fichier)
        return data
    else:
        return None

# Charger les données
data = charger_fichier()

if data is not None:
    
    # Afficher les données nettoyées
    st.subheader("Aperçu des données :")
    st.dataframe(data)

    # Sélectionner le type de dispositif expérimental
    dispositif = st.radio(
        "Sélectionnez le type de dispositif expérimental :",
        ["DCA", "DBAC", "Split Plot"]
    )

    # Colonnes disponibles
    colonnes = data.columns.tolist()

    # Section des facteurs : Limitation à 2 facteurs
    facteurs = st.multiselect("Sélectionnez jusqu'à 2 facteurs à analyser", colonnes, max_selections=2)

    # Exclure les facteurs sélectionnés de la liste des choix pour le bloc
    colonnes_sans_facteurs = [col for col in colonnes if col not in facteurs]

    # Gestion des dispositifs spécifiques
    facteur_bloc = None
    if dispositif in ["DBAC", "Split Plot"]:
        facteur_bloc = st.selectbox("Sélectionnez la colonne représentant le bloc :", colonnes_sans_facteurs)

    # Section des variables à analyser
    variables_numeriques = [col for col in colonnes if data[col].dtype in ["float64", "int64"]]
    variables = st.multiselect("Sélectionnez les colonnes à analyser (variables)", variables_numeriques)

    if facteurs and variables:
        st.write(f"Facteurs sélectionnés : {facteurs}")
        st.write(f"Variables sélectionnées : {variables}")

        for variable in variables:
            st.subheader(f"Analyse des données pour la variable : {variable}")

            try:
                if len(facteurs) == 1:
                    # Vérifier le nombre de modalités du facteur
                    facteur = facteurs[0]
                    modalites = data[facteur].nunique()

                    if modalites == 2:
                        # Test t de Student pour un facteur avec 2 modalités
                        st.write("Deux modalités pour ce facteur, un test t de Student sera effectué.")
                        groupe1 = data[data[facteur] == data[facteur].unique()[0]][variable]
                        groupe2 = data[data[facteur] == data[facteur].unique()[1]][variable]
                        t_stat, p_val = stats.ttest_ind(groupe1, groupe2)

                        st.write(f"t-statistique: {t_stat}")
                        st.write(f"p-value: {p_val}")
                        if p_val < 0.05:
                            st.success("Les moyennes des deux groupes sont significativement différentes.")
                        else:
                            st.warning("Les moyennes des deux groupes ne sont pas significativement différentes.")

                        # Visualisation
                        st.write("### Visualisation graphique")
                        grouped = data.groupby(facteur)[variable].agg(["mean", "std"]).reset_index()

                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.barplot(
                            x=facteur,
                            y="mean",
                            data=grouped,
                            ci=None,
                            palette="muted"
                        )

                        # Ajouter des barres d'écart-type
                        for i, row in grouped.iterrows():
                            ax.errorbar(
                                x=i,
                                y=row["mean"],
                                yerr=row["std"],
                                fmt='none',
                                ecolor='black',
                                capsize=5
                            )

                        ax.set_title(f"Moyenne et écart-type ({facteur})")
                        ax.set_ylabel(variable)
                        ax.set_xlabel(facteur)
                        st.pyplot(fig)

                    else:
                        # ANOVA pour un facteur avec plus de 2 modalités
                        st.write(f"Plus de 2 modalités pour {facteur}, une ANOVA sera effectuée.")
                        facteurs_formule = f"C({facteur})"
                        formule = f"{variable} ~ {facteurs_formule}"

                        model = ols(formule, data=data).fit()
                        anova_table = sm.stats.anova_lm(model, typ=3)

                        st.write("### Tableau ANOVA complet")
                        st.write(anova_table)
                        if anova_table.loc[f"C({facteur})", 'PR(>F)'] < 0.05:
                                st.success(f"L'effet du facteur {facteur} est significatif (p < 0.05).")
                        else:
                                st.warning(f"L'effet du facteur {facteur} n'est pas significatif.")
                        # Visualisation graphique
                        st.write("### Visualisation graphique")
                        grouped = data.groupby(facteur)[variable].agg(["mean", "std"]).reset_index()

                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.barplot(
                            x=facteur,
                            y="mean",
                            data=grouped,
                            ci=None,
                            palette="muted"
                        )

                        # Ajouter des barres d'écart-type
                        for i, row in grouped.iterrows():
                            ax.errorbar(
                                x=i,
                                y=row["mean"],
                                yerr=row["std"],
                                fmt='none',
                                ecolor='black',
                                capsize=5
                            )

                        ax.set_title(f"Moyenne et écart-type ({facteur})")
                        ax.set_ylabel(variable)
                        ax.set_xlabel(facteur)
                        st.pyplot(fig)

                elif len(facteurs) == 2:
                    # Cas de deux facteurs
                    st.write("Deux facteurs sélectionnés, une ANOVA avec interaction sera effectuée.")
                    facteur1, facteur2 = facteurs
                    # Créer une formule d'interaction
                    interaction_formule = ":".join([f"C({facteur})" for facteur in facteurs])
                    facteurs_formule = " + ".join([f"C({facteur})" for facteur in facteurs])

                    formule = f"{variable} ~ {facteurs_formule} + {interaction_formule}"

                    model = ols(formule, data=data).fit()
                    anova_table = sm.stats.anova_lm(model, typ=3)

                    st.write("### Tableau ANOVA complet")
                    st.write(anova_table)

                    # Vérifier l'interaction
                    if interaction_formule in anova_table.index and anova_table.loc[interaction_formule, 'PR(>F)'] < 0.05:
                        st.success(f"L'effet d'interaction entre {facteur1} et {facteur2} est significatif (p < 0.05).")
                    else:
                        st.info(f"L'effet d'interaction n'est pas significatif. Analyse des facteurs individuels :")
                        for facteur in facteurs:
                            if anova_table.loc[f"C({facteur})", 'PR(>F)'] < 0.05:
                                st.success(f"L'effet du facteur {facteur} est significatif (p < 0.05).")
                            else:
                                st.warning(f"L'effet du facteur {facteur} n'est pas significatif.")

                    # Visualisation graphique
                    st.write("### Visualisation graphique")
                    data["Combinaison"] = data[facteur1].astype(str) + " - " + data[facteur2].astype(str)

                    grouped = data.groupby("Combinaison")[variable].agg(["mean", "std"]).reset_index()

                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(
                        x="Combinaison",
                        y="mean",
                        data=grouped,
                        ci=None,
                        palette="muted"
                    )

                    # Ajouter des barres d'écart-type manuelles
                    for i, row in grouped.iterrows():
                        ax.errorbar(
                            x=i,
                            y=row["mean"],
                            yerr=row["std"],
                            fmt='none',
                            ecolor='black',
                            capsize=5
                        )

                    ax.set_title(f"Moyenne et écart-type combinés ({facteur1} et {facteur2})")
                    ax.set_ylabel(variable)
                    ax.set_xlabel("Combinaisons des modalités")
                    ax.set_xticklabels(grouped["Combinaison"], rotation=45, ha="right")  # Rotation des étiquettes
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")
