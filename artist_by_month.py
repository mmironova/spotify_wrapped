import json 
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

data_path="/Users/mironova/Documents/spotify2024/"
f=open(data_path+"StreamingHistory_music_0.json")
df = pd.read_json(f)

for j in range(1,7):
	print(j)
	f=open(data_path+"StreamingHistory_music_%s.json"%j)
	df2 = pd.read_json(f)
	df=pd.concat([df,df2], ignore_index=True)

df["endTime"]=pd.to_datetime(df["endTime"])


weeks = set(list(df["endTime"].dt.week))

top_week=[]

for i in weeks:
	df_of_that_week = df[(df['endTime'].dt.week == i) & (df['msPlayed']> 10000)]
	max_df=df_of_that_week.groupby(['artistName'])['artistName'].count().reset_index(name='Count').sort_values(['Count'], ascending=False)
	total_play=max_df['Count'].sum()
	max_df['Frac']=max_df['Count']/total_play*100
	print(max_df.head(1))
	l1=max_df.iloc[0].tolist()
	l2=max_df.iloc[1].tolist()
	l3=max_df.iloc[2].tolist()
	if l1[1]<3: 
		l1[0]=""
	if l2[1]<3: 
		l2[0]=""	
	if l3[1]<3: 
		l3[0]=""
	if float(len(l1[0]))/float(l1[1])>3 and l1[1]<5: 
		l1[0]=""
	if float(len(l2[0]))/float(l2[1])>3 and l2[1]<5: 
		l2[0]=""	
	if float(len(l3[0]))/float(l3[1])>3 and l3[1]<5: 
		l3[0]=""
	if "Planes" in l1[0]:
		l1[0]=""	
	week=df_of_that_week["endTime"].head(1).dt.strftime("%d/%m/%Y").tolist()[0]
	top_week.append(
    {
    	'time':week,
        'track1': l1[0][0:25],
        'Top 1': l1[1],
        'track2': l2[0][0:25],
        'Top 2': l2[1],
        'track3': l3[0][0:25],
        'Top 3': l3[1]
    }
	)		
   #display(df_of_that_week)

top_week_df=pd.DataFrame(top_week)
ax = top_week_df.plot(kind='barh', stacked=True, figsize=(11, 7), rot=90, xlabel='Plays', ylabel='Weeks', color=['pink','plum','lightsteelblue'],width=0.9)
k=0
for c in ax.containers:
	print(c)
    # remove the labels parameter if it's not needed for customized labels
	if k==0:
		ax.bar_label(c, labels=top_week_df['track1'].tolist(), label_type='center',fontsize=8,color="mediumvioletred")
	if k==1:
		ax.bar_label(c, labels=top_week_df['track2'].tolist(), label_type='center',fontsize=8,color='purple')
	if k==2:
		ax.bar_label(c, labels=top_week_df['track3'].tolist(), label_type='center',fontsize=8,color='midnightblue')

	k=k+1

ax.set_yticklabels(top_week_df['time'].tolist(),rotation=0,fontsize=10)
plt.gca().invert_yaxis()
plt.subplots_adjust(left=0.2)
plt.tight_layout()
plt.savefig('artists.png',dpi=400)
plt.show()




