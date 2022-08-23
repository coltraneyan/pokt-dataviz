import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns

pokt_sd_data = pd.read_csv("POKT-Supply-Demand.csv")
pokt_pr_data = pd.read_csv("POKT-Token-Price.csv")

# cleaning data for both dataframes

# supply demand dataset
pokt_sd_data["Day"] = pd.to_datetime(pokt_sd_data["Day"])
pokt_sd_data = pokt_sd_data[~(pokt_sd_data['Day'] < '2022-01-13')]
pokt_sd_data.rename(columns={"Day": "Date"}, inplace=True)
pokt_sd_data["Day"] = pokt_sd_data["Date"].dt.date
pokt_sd_data["Month"] = pokt_sd_data["Date"].dt.month

# token price dataset
pokt_pr_data["Date"] = pd.to_datetime(pokt_pr_data["Date"])
pokt_pr_data = pokt_pr_data.sort_values(by="Date")
pokt_pr_data = pokt_pr_data[~(pokt_pr_data["Date"] > '2022-06-30')]
pokt_pr_data["Day"] = pokt_pr_data["Date"].dt.date
pokt_pr_data["Month"] = pokt_pr_data["Date"].dt.month
pokt_pr_data["Close**"] = pokt_pr_data["Close**"].str.replace('$', '').astype(float)

# adding relays data columns
pokt_sd_data["Total Relays"] = pokt_sd_data.loc[:,pokt_sd_data.columns.str.contains("Relays")].sum(axis=1).astype(int)
pokt_sd_data["POKT Supply Increase"] =  pokt_sd_data["POKT Supply Increase"].str.replace(',', '').astype(int)
pokt_sd_data["dApp Staked Demand (POKT)"] =  pokt_sd_data["dApp Staked Demand (POKT)"].str.replace(',', '').astype(int)

pokt_sd_data["Relays per Token Issued"] = pokt_sd_data["Total Relays"]/pokt_sd_data["POKT Supply Increase"]
pokt_sd_data["Relays per Demand Token Staked"] = pokt_sd_data["Total Relays"]/pokt_sd_data["dApp Staked Demand (POKT)"]

# display supply + demand dataframe
pokt_sd_data

# display price dataframe
pokt_pr_data

# data viz

# seaborn constants
sns.set_theme(style="darkgrid", font="monospace")
sns.set_context( font_scale = 1)
plt.rc("grid", linewidth=5)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('date.autoformatter', day='%b %Y')

figsize=(10,6)
months = [pd.datetime(2022, 1, 1), pd.datetime(2022, 2, 1), pd.datetime(2022, 3, 1), 
          pd.datetime(2022, 4, 1), pd.datetime(2022, 5, 1), pd.datetime(2022, 6, 1), 
          pd.datetime(2022, 7, 1)];
xlim_right = pd.datetime(2022, 7, 1)

# price plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_pr_data["Day"], pokt_pr_data["Close**"], ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([0.50, 1.00, 1.50, 2.00, 2.50, 3.00])
plt.xlim(None, xlim_right)
plt.ylim(0, 3)
sns.despine(left=True)
plt.title('Price (USD)')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('price.png')

# demand staked plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_sd_data["Day"], pokt_sd_data["dApp Staked Demand (POKT)"], ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([26200000, 26450000, 26700000])
plt.ticklabel_format(axis="y", style="plain")
plt.xlim(None, xlim_right)
plt.ylim(26200000, 26700000)
sns.despine(left=True)
plt.title('Staked Tokens by dApps')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('real-supply-increase.png')

# relays per stake plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_sd_data["Day"], pokt_sd_data["Relays per Demand Token Staked"], ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([25, 50, 75, 100])
plt.xlim(None, xlim_right)
plt.ylim(0, 100)
sns.despine(left=True)
plt.title('Relays / POKT Staked (dApps Only)')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('demand-relays.png')

# relays per rewards plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_sd_data["Day"], pokt_sd_data["Relays per Token Issued"], ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([250, 500, 750, 1000])
plt.xlim(None, xlim_right)
plt.ylim(0, 1000)
sns.despine(left=True)
plt.title('Relays / POKT Issued')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('supply-relays.png')

# total relays plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_sd_data["Day"], pokt_sd_data["Total Relays"], ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([500000000, 1000000000, 1500000000, 2000000000, 2500000000])
plt.ticklabel_format(axis="y", style="plain")
plt.xlim(None, xlim_right)
plt.ylim(0, 2500000000)
sns.despine(left=True)
plt.title('Total Relays')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('total-relays.png')

# supply increase plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_sd_data["Day"], pokt_sd_data["POKT Supply Increase"], ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000])
plt.ticklabel_format(axis="y", style="plain")
plt.xlim(None, xlim_right)
plt.ylim(0, 7000000)
sns.despine(left=True)
plt.title('POKT Supply Increase')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('supply-increase.png')

# real supply increase plot

plt.figure(figsize=figsize)
sns.lineplot(pokt_sd_data["Day"], (np.array(pokt_pr_data["Close**"]) * np.array(pokt_sd_data["POKT Supply Increase"])), ci=None, linewidth=3)
plt.xticks(months)
plt.yticks([1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 11000000])
plt.ticklabel_format(axis="y", style="plain")
plt.xlim(None, xlim_right)
plt.ylim(0, 11000000)
sns.despine(left=True)
plt.title('Real Value of POKT Supply Increase')
plt.xlabel('')
plt.ylabel('')
plt.tight_layout()
# plt.savefig('real-supply-increase.png')
