AUTHOR = "KHARRAZI ADAM"
EMAIL = "adamkharrazi401@gmail.com"

import streamlit as st
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Analyse Statistique pour les Expérimentations Agronomiques 1.0")

def charger_fichier():
    fichier = st.file_uploader("Chargez un fichier Excel", type=["xlsx", "xls"])
    if fichier is not None:
        data = pd.read_excel(fichier)
        return data
    else:
        return None

data = charger_fichier()

if data is not None:
    
    st.subheader("Aperçu des données :")
    st.dataframe(data)

    dispositif = st.radio(
        "Sélectionnez le type de dispositif expérimental :",
        ["DCA", "DBAC", "Split Plot"]
    )

    colonnes = data.columns.tolist()

    facteurs = st.multiselect("Sélectionnez jusqu'à 2 facteurs à analyser", colonnes, max_selections=2)

    colonnes_sans_facteurs = [col for col in colonnes if col not in facteurs]

    facteur_bloc = None
    if dispositif in ["DBAC", "Split Plot"]:
        facteur_bloc = st.selectbox("Sélectionnez la colonne représentant le bloc :", colonnes_sans_facteurs)

    variables_numeriques = [col for col in colonnes if data[col].dtype in ["float64", "int64"]]
    variables = st.multiselect("Sélectionnez les colonnes à analyser (variables)", variables_numeriques)

    if facteurs and variables:
        st.write(f"Facteurs sélectionnés : {facteurs}")
        st.write(f"Variables sélectionnées : {variables}")

        for variable in variables:
            st.subheader(f"Analyse des données pour la variable : {variable}")

            try:
                # Cas DCA 
                if dispositif == "DCA":
                    if len(facteurs) == 1:
                        facteur = facteurs[0]
                        modalites = data[facteur].nunique()

                        # Si 2 modalités, faire un test t de Student
                        if modalites == 2:
                            st.write("Deux modalités pour ce facteur en DCA, un test t de Student sera effectué.")
                            groupe1 = data[data[facteur] == data[facteur].unique()[0]][variable]
                            groupe2 = data[data[facteur] == data[facteur].unique()[1]][variable]
                            t_stat, p_val = stats.ttest_ind(groupe1, groupe2)

                            st.write(f"t-statistique: {t_stat}")
                            st.write(f"p-value: {p_val}")
                            if p_val < 0.05:
                                st.success("Les moyennes des deux groupes sont significativement différentes.")
                            else:
                                st.warning("Les moyennes des deux groupes ne sont pas significativement différentes.")
                        else:
                            # Sinon, faire ANOVA 1
                            st.write(f"Plus de 2 modalités pour {facteur}, une ANOVA 1 sera effectuée.")
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
                    
                    # Cas avec 2 facteurs pour DCA
                    elif len(facteurs) == 2:
                        st.write("Deux facteurs sélectionnés, une ANOVA 2 sera effectuée.")
                        
                        formule = f"{variable} ~ C({facteurs[0]}) + C({facteurs[1]}) + C({facteurs[0]}):C({facteurs[1]})"
                        model = ols(formule, data=data).fit()
                        anova_table = sm.stats.anova_lm(model, typ=3)

                        st.write("### Tableau ANOVA complet")
                        st.write(anova_table)

                        interaction_formule = f"C({facteurs[0]}):C({facteurs[1]})"
                        if interaction_formule in anova_table.index and anova_table.loc[interaction_formule, 'PR(>F)'] < 0.05:
                            st.success(f"L'effet d'interaction entre {facteurs[0]} et {facteurs[1]} est significatif (p < 0.05).")
                        else:
                            st.info(f"L'effet d'interaction n'est pas significatif. Analyse des facteurs individuels :")
                            for facteur in facteurs:
                                if anova_table.loc[f"C({facteur})", 'PR(>F)'] < 0.05:
                                    st.success(f"L'effet du facteur {facteur} est significatif (p < 0.05).")
                                else:
                                    st.warning(f"L'effet du facteur {facteur} n'est pas significatif.")

                        
                # Cas DBAC 
                elif dispositif == "DBAC":
                    if len(facteurs)==1:
                        st.write("Un facteur sélectionné, une ANOVA 1 sera effectuée.")
                        formule = f"{variable} ~ C({facteurs[0]}) + C({facteur_bloc})"
                    elif len(facteurs) == 2:
                        st.write("Deux facteurs sélectionnés, une ANOVA 2 sera effectuée.")
                        formule = f"{variable} ~ C({facteurs[0]}) + C({facteurs[1]}) + C({facteur_bloc}) + C({facteurs[0]}):C({facteurs[1]})"
                
                    model = ols(formule, data=data).fit()
                    anova_table = sm.stats.anova_lm(model, typ=3)

                    st.write("### Tableau ANOVA complet")
                    st.write(anova_table)

                    interaction_formule = f"C({facteurs[0]}):C({facteurs[1]})"
                    if interaction_formule in anova_table.index and anova_table.loc[interaction_formule, 'PR(>F)'] < 0.05:
                        st.success(f"L'effet d'interaction entre {facteurs[0]} et {facteurs[1]} est significatif (p < 0.05).")
                    else:
                        st.info(f"L'effet d'interaction n'est pas significatif. Analyse des facteurs individuels :")
                        for facteur in facteurs:
                            if anova_table.loc[f"C({facteur})", 'PR(>F)'] < 0.05:
                                st.success(f"L'effet du facteur {facteur} est significatif (p < 0.05).")
                            else:
                                st.warning(f"L'effet du facteur {facteur} n'est pas significatif.")

                # Cas Split Plot 
                elif dispositif == "Split Plot" and len(facteurs)==2 :
                    st.write("Deux facteurs sélectionnés, une ANOVA 2 sera effectuée.")
                    formule = f"{variable} ~ C({facteurs[0]}) + C({facteurs[1]}) + C({facteur_bloc}) + C({facteurs[0]}):C({facteur_bloc}) + C({facteurs[0]}):C({facteurs[1]})"
                
                    model = ols(formule, data=data).fit()
                    anova_table = sm.stats.anova_lm(model, typ=3)

                    st.write("### Tableau ANOVA complet")
                    st.write(anova_table)
                    interaction_formule = f"C({facteurs[0]}):C({facteurs[1]})"
                    if interaction_formule in anova_table.index and anova_table.loc[interaction_formule, 'PR(>F)'] < 0.05:
                        st.success(f"L'effet d'interaction entre {facteurs[0]} et {facteurs[1]} est significatif (p < 0.05).")
                    else:
                        st.info(f"L'effet d'interaction n'est pas significatif. Analyse des facteurs individuels :")
                        for facteur in facteurs:
                            if anova_table.loc[f"C({facteur})", 'PR(>F)'] < 0.05:
                                st.success(f"L'effet du facteur {facteur} est significatif (p < 0.05).")
                            else:
                                st.warning(f"L'effet du facteur {facteur} n'est pas significatif.")

                 #Visualisation
                if len(facteurs)==1 :
                        st.write("### Visualisation graphique")
                        grouped = data.groupby(facteurs[0])[variable].agg(["mean", "std"]).reset_index()
                        fig, ax = plt.subplots(figsize=(8, 6))
                        sns.barplot(
                            x=facteurs[0],
                            y="mean",
                            data=grouped,
                            ci=None,
                            palette="muted"
                        )
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

                elif len(facteurs)==2 :
                    st.write("### Visualisation graphique")
                    data["Combinaison"] = data[facteurs[0]].astype(str) + " - " + data[facteurs[1]].astype(str)
                    grouped = data.groupby("Combinaison")[variable].agg(["mean", "std"]).reset_index()
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(
                            x="Combinaison",
                            y="mean",
                            data=grouped,
                            ci=None,
                            palette="muted"
                        )
                    for i, row in grouped.iterrows():
                            ax.errorbar(
                                x=i,
                                y=row["mean"],
                                yerr=row["std"],
                                fmt='none',
                                ecolor='black',
                                capsize=5
                            )
                    ax.set_title(f"Moyenne et écart-type combinés ({facteurs[0]} et {facteurs[1]})")
                    ax.set_ylabel(variable)
                    ax.set_xlabel("Combinaisons des modalités")
                    ax.set_xticklabels(grouped["Combinaison"], rotation=45, ha="right")
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
