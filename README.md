# Agronomic_Statistical_Analysis
Application interactive conçue pour faciliter l'analyse statistique des données issues d'expérimentations agronomiques. Elle permet d'effectuer des tests ANOVA et t de Student, de visualiser les résultats sous forme de graphiques clairs et de gérer différents dispositifs expérimentaux.

Before running the program, make sure to install the necessary requirements.
First, ensure you have Python 3.x or above installed.

Run the following commands to install the required libraries:

pip install streamlit ;  
pip install pandas ;  
pip install statsmodels ;  
pip install matplotlib ;  
pip install seaborn ;  
pip install scipy   

- Instructions  
1. Préparation de la base de données :  
Le fichier Excel doit commencer à la cellule A1.  
Les noms des colonnes doivent :
Être en minuscules.  
Ne pas contenir d'espaces ou de caractères spéciaux (ex. : utilisez _ pour séparer les mots).  
2. Analyse statistique :  
Nombre maximal de facteurs :
Deux facteurs maximum, quel que soit le dispositif expérimental (DCA, DBAC ou Split-Plot).
Pour DBAC et Split-Plot, un bloc est ajouté.  
Tests appliqués :
Si un seul facteur avec deux modalités est sélectionné : un T-Test est appliqué.
Sinon :
ANOVA à un facteur (pour un seul facteur avec plusieurs modalités).
ANOVA à deux facteurs (pour deux facteurs).  
3. Vérification des interactions :
L'analyse commence par vérifier l'interaction entre les facteurs (si deux facteurs sont choisis).
Si l'interaction est significative : pas besoin d'analyser les effets individuels des facteurs.
Si l'interaction est non significative : les effets individuels sont analysés séparément.  
4. Considérations spécifiques :
Split-Plot :
Le premier facteur sélectionné est considéré comme primaire.
Le deuxième facteur sélectionné est considéré comme secondaire.
Obligatoire : choisir deux facteurs + un bloc.  
Cohérence : soyez rigoureux dans vos sélections pour garantir des résultats valides.  
Contact  
Pour plus de détails, des remarques ou des améliorations, veuillez contacter :
📧 Adam Kharrazi  
adamkharrazi401@gmail.com  

Avertissement  
Ce projet est conçu pour des expérimentations agronomiques spécifiques. Respectez les consignes ci-dessus pour garantir des résultats fiables.  
