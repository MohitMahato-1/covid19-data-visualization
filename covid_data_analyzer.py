import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("COVID_19.csv")
#Confirmed cases barchart
top10=df.nlargest(10,"Confirmed")
plt.figure(figsize=(10,5))
plt.bar(top10["Country/Region"],top10["Confirmed"],color="red")
plt.title(" Top 10 Confirmed cases of Covid-19")
plt.xlabel("Countries")
plt.ylabel("Confirmed cases in Number")
plt.xticks(rotation = 45)
plt.yticks(rotation = 60)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
                                    )
plt.show()

#Death V/S Recovery barchart

plt.figure(figsize=(10,5))
plt.bar(top10["Country/Region"],top10["Deaths"],label="deaths",color="black")
plt.bar(top10["Country/Region"],top10["Recovered"],label="Recovered",color="green",alpha=0.7)
plt.title("Death v/s Recovery")
plt.xlabel("country")
plt.ylabel("Death vs Recovery")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#3 Pie Chart

region_cases = df.groupby("WHO Region")["Confirmed"].sum()

plt.figure(figsize=(8,8))
plt.pie(region_cases, labels=region_cases.index, autopct="%1.1f%%")
plt.title("Region Wise cases")
plt.tight_layout()
plt.show()

#Scatter Plot

plt.figure(figsize=(8,5))
plt.scatter(df["Confirmed"],df["Deaths"],color="red",alpha=0.5)
plt.title("Scatter Plot Deaths vs Confirmed")
plt.xlabel("Death")
plt.ylabel("Confrimed")
plt.tight_layout()
plt.show()

#Bar chart Horizontal 
top_10death=df.nlargest(10,"Deaths")
#plt.barh(Y axis, X axis)
    #     names   numbers
plt.figure(figsize=(8,5))
plt.barh(top_10death["Country/Region"], top_10death["Deaths"],color="darkred")  
plt.title("Horizontal barchart for death")
plt.xlabel("Deaths")
plt.tight_layout()
plt.show()