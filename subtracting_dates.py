import pandas as pd

df = pd.read_csv('202006-divvy-tripdata.csv')

df1 = df[['started_at', 'ended_at', 'member_casual']]

start_df = df1['started_at'].str.split(" ", n = 1, expand = True)
df["start_date"] = start_df[0]
df["start_time"] = start_df[1]

end_df = df1['ended_at'].str.split(" ", n = 1, expand = True)
df["end_date"] = end_df[0]
df["end_time"] = end_df[1]

start_date_df = df['start_date'].str.split("-", expand = True)
df["start_year"] = start_date_df[0].astype(str).astype(int)
df["start_month"] = start_date_df[1].astype(str).astype(int)
df["start_day"] = start_date_df[2].astype(str).astype(int)

start_time_df = df['start_time'].str.split(":", expand = True)
df["start_hour"] = start_time_df[0].astype(str).astype(int)
df["start_minute"] = start_time_df[1].astype(str).astype(int)
df["start_second"] = start_time_df[2].astype(str).astype(int)

end_date_df = df['end_date'].str.split("-", expand = True)
df["end_year"] = end_date_df[0].astype(str).astype(int)
df["end_month"] = end_date_df[1].astype(str).astype(int)
df["end_day"] = end_date_df[2].astype(str).astype(int)

end_time_df = df['end_time'].str.split(":", expand = True)
df["end_hour"] = end_time_df[0].astype(str).astype(int)
df["end_minute"] = end_time_df[1].astype(str).astype(int)
df["end_second"] = end_time_df[2].astype(str).astype(int)

def duration(syear,smon,sday,shour,smin,ssec,eyear,emon,eday,ehour,emin,esec):
    if ((esec - ssec) < 0):
        emin -= 1
        sec = (esec + 60) - ssec
    else:
        sec = esec - ssec
    if ((emin - smin) < 0):
        ehour -= 1
        min = (emin + 60) - smin
    else:
        min = emin - smin
    if ((ehour - shour) < 0):
        eday -= 1
        hour = (ehour + 24) - shour
    else:
        hour = ehour - shour
    if ((eday - sday) < 0):
        if (smon in [1,3,5,7,8,10,12]):
            emon -= 1
            day = (eday + 31) - sday
        elif (smon in [4,6,9,11]):
            emon -= 1
            day = (eday + 30) - sday
        else:
            emon -= 1
            day = (eday + 28) - sday
    else:
        day = eday - sday
    if ((emon - smon) < 0):
        eyear -= 1
        mon = (emon + 12) - smon
    else:
        mon = emon - smon
    year = eyear - syear
    return [year, mon, day, hour, min, sec]

dur_list = []

for ind in df.index:
    dur = duration(df['start_year'][ind],df['start_month'][ind],df['start_day'][ind],df['start_hour'][ind],df['start_minute'][ind],df['start_second'][ind],df['end_year'][ind],df['end_month'][ind],df['end_day'][ind],df['end_hour'][ind],df['end_minute'][ind],df['end_second'][ind])
    dur_list.append(dur)

time_data = pd.DataFrame(dur_list, columns=['year','month','day','hour','minute','second'])
time_data['started_at'] = df['started_at']
time_data['ended_at'] = df['ended_at']
time_data['member_casual'] = df['member_casual']

time_data.to_csv( "time_data202006.csv", index=False, encoding='utf-8-sig')