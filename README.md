# Agronomic_Statistical_Analysis
Interactive application designed to facilitate the statistical analysis of data from agronomic experiments. It allows users to perform ANOVA and Student's t-tests, visualize results through clear graphs, and manage various experimental designs.

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
- 
1. Preparing the Database:

The Excel file must start at cell A1.
Column names must:
Be in lowercase.
Contain no spaces or special characters (e.g., use _ to separate words).

2. Statistical Analysis:

Maximum number of factors: Two factors maximum, regardless of the experimental design (CRD, RCBD, or Split-Plot).
For RCBD and Split-Plot designs, a block is added.

Applied tests:
If a single factor with two levels is selected: a T-Test is applied.

Otherwise:
One-way ANOVA (for a single factor with multiple levels).
Two-way ANOVA (for two factors).

3. Checking for Interactions:

The analysis starts by checking the interaction between the factors (if two are selected).
If the interaction is significant: there’s no need to analyze individual factor effects.
If the interaction is not significant: individual effects are analyzed separately.

4. Specific Considerations:

Split-Plot:
The first selected factor is considered the main factor.
The second is considered the sub-factor.
Required: two factors + one block.

Consistency: Be rigorous in your selections to ensure valid results.

Contact
For more details, feedback, or suggestions:
📧 Adam Kharrazi
adamkharrazi401@gmail.com

Disclaimer
This project is designed for specific agronomic experiments. Please follow the instructions above to ensure reliable results.
