import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Italy_total_emissions.csv", 
                 sep = ",", 
                 usecols=["Unit of measure", "Air pollutants and greenhouse gases", 
                          "Source sectors for greenhouse gas emissions (Common reporting format, UNFCCC)", 
                          "geo", "Geopolitical entity (reporting)", "TIME_PERIOD", "OBS_VALUE"])

df.rename(columns={"Unit of measure": "Unit", 
                   "Air pollutants and greenhouse gases":"Air pollutants and GHG",
                   "Source sectors for greenhouse gas emissions (Common reporting format, UNFCCC)":"Source sectors for GHG emissions",
                   "Geopolitical entity (reporting)":"Country",
                   "TIME_PERIOD":"Year"}, 
                   inplace=True)

print(df.info())
print(df.head(5))
print(df["Unit"].unique())

#Missing values
print(df.isna().sum()) #0 missing values
df_filled = df.dropna(subset=['OBS_VALUE']) 
print(df_filled.isna().sum())

#Change data type for year
df_filled["Year"] = df_filled["Year"].astype(int)

#Analysis
#Percentage emission reduction from oldest to latest year
oldest_year = df_filled["Year"].min()
emissions_oldest_year = df_filled.loc[df_filled["Year"] == oldest_year, "OBS_VALUE"].values[0]

latest_year = df_filled["Year"].max()
emissions_latest_year = df_filled.loc[df_filled["Year"] == latest_year, "OBS_VALUE"].values[0]

reduction = - (emissions_latest_year - emissions_oldest_year) / emissions_oldest_year
print(f"GHG emission Italian reduction from {oldest_year} to {latest_year}: {reduction:.2%}")

#3 years with biggest decrease
df_filled = df_filled.sort_values("Year")
df_filled["Annual_change"] = df_filled["OBS_VALUE"].diff()
df_filled["Annual_pct_change"] = df_filled["OBS_VALUE"].pct_change()
top3_reductions = df_filled.nsmallest(3, "Annual_pct_change")
print(top3_reductions[["Year", "Annual_pct_change"]])


#Plots
# Total annual emissions
plot = df_filled.plot(x='Year', y='OBS_VALUE', 
        kind='line', 
        title='Total GHG Emissions by Year [1990-2023] - Italy',
        marker='o',
        ylabel='Emissions [Thousand Tonnes]')

plt.xticks(range(oldest_year, latest_year + 1, 5))
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('Italy_yearly_emissions.png')
plt.show()

#Annual reductions
ax = df_filled.plot(
    x='Year',
    y='Annual_pct_change',
    kind='line',
    title='Annual GHG Reduction [1990-2023] - Italy',
    ylabel='% Reduction'
)

scatter = ax.scatter(
    top3_reductions["Year"],
    top3_reductions["Annual_pct_change"],
    color='red',
    marker='D',
    s=100,
    label='Top 3 Largest Reductions'
)

plt.xticks(range(oldest_year, latest_year + 1, 5))
plt.grid(True, linestyle='--', alpha=0.5)
ax.legend([scatter], ['Top 3 Largest Reductions'])
plt.savefig('Italy_annual_reduction_emissions.png')
plt.show()