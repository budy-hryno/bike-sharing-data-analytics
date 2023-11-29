import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

def create_daily_users_df(df):
    daily_users_df = df.resample(rule="D", on="date").agg({
        "total_user": "sum",
        "casual_user": "sum",
        "registered_user": "sum",
    })

    daily_users_df = daily_users_df.reset_index()
    daily_users_df.rename(columns={
        "total_user": "users_sum",
        "casual_user": "casual_sum",
        "registered_user": "registered_sum",
    }, inplace=True)

    return daily_users_df

def create_sum_season_df(df):
    sum_season_df = df.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()

    return sum_season_df

def create_sum_hour_df(df):
    # jumlah pengguna terbanyak berdasarkan jam
    sum_hour_df = df.groupby("hour").total_user.sum().sort_values(ascending=False).reset_index()
    # kolom hour diubah jadi string supaya grafiknya tidak otomotis urut berdasarkan hour
    sum_hour_df["hour"] = sum_hour_df["hour"].astype(str)

    # invers untuk jumlah pengguna terendah berdasarkan jam
    inversed_sum_hour_df = df.groupby("hour").total_user.sum().sort_values(ascending=True).reset_index()
    # kolom hour diubah jadi string supaya grafiknya tidak otomotis urut berdasarkan hour
    inversed_sum_hour_df["hour"] = inversed_sum_hour_df["hour"].astype(str)

    return sum_hour_df, inversed_sum_hour_df

def create_sum_weather_df(df):
    sum_weather_df = df.groupby("weather").total_user.sum().sort_values(ascending=False).reset_index()

    return sum_weather_df
    
def create_sum_temp_df(df):
    sum_temp_df = df.groupby("temp_group").total_user.sum().sort_values(ascending=False).reset_index()

    return sum_temp_df

# load clean data
day_df = pd.read_csv("clean_data/day_clean.csv")
hour_df = pd.read_csv("clean_data/hour_clean.csv")

# sort data dan memastikan kolom date bertipe datetime
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)

day_df["date"] = pd.to_datetime(day_df["date"])
hour_df["date"] = pd.to_datetime(hour_df["date"])

day_min_date = day_df["date"].min()
day_max_date = day_df["date"].max()

hour_min_date = hour_df["date"].min()
hour_max_date = hour_df["date"].max()

# BUTUH EDIT
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.ibb.co/d0Dyxqv/image-2023-11-28-224139077.png", width=290)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',min_value=day_min_date,
        max_value=day_max_date,
        value=[day_min_date, day_max_date]
    )

main_day_df = day_df[(day_df["date"] >= str(start_date)) &  
                     (day_df["date"] <= str(end_date))]

main_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                       (hour_df["date"] <= str(end_date))]

# define dataframe yang dibutuhkan
daily_users_df = create_daily_users_df(main_day_df)
sum_season_df = create_sum_season_df(main_day_df)
sum_hour_df, inversed_sum_hour_df = create_sum_hour_df(main_hour_df)
sum_weather_df = create_sum_weather_df(main_hour_df)
sum_temp_df = create_sum_temp_df(main_hour_df)


#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Share Dashboard :bicyclist:')

#1
st.subheader('Daily Bike Sharing User')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_user = daily_users_df.users_sum.sum()
    st.metric("Total Sharing Bike", value=total_user)

with col2:
    total_sum = daily_users_df.registered_sum.sum()
    st.metric("Total Registered User", value=total_sum)

with col3:
    total_sum = daily_users_df.casual_sum.sum()
    st.metric("Total Casual User", value=total_sum)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["date"],
    daily_users_df["users_sum"],
    marker='o', 
    linewidth=2,
    color="#df9c20"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

#2
st.subheader("Jumlah Pengguna Bike Sharing Berdasarkan Musim")
# define objek grafik
fig = plt.figure(figsize=(10, 5))

# define data terkait ke grafik batang
ax = sns.barplot(
    y="total_user",
    x="season",
    data=sum_season_df,
    color="#ffd080"
)

# mencari record dengan jumlah pengguna tertinggi
max_index = sum_season_df['total_user'].idxmax()
min_index = sum_season_df['total_user'].idxmin()

# atur warna bar tertinggi menjadi berbeda
ax.patches[max_index].set_facecolor('#df9c20')
ax.patches[min_index].set_facecolor('#df9c20')

# format titik pada angka ribuan
ax.yaxis.set_major_formatter('{x:,.0f}')

# pembentukan visual grafik
plt.title("Jumlah Pengguna berdasarkan Musim", loc="center", fontsize=18, fontweight=600)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#3
st.subheader("Jumlah Pengguna Bike Sharing Berdasarkan Jam")

# define objek grafik
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 8))

# grafik 1: jam dengan pengguna rental sepeda terbanyak
sns.barplot(x="hour", y="total_user", data=sum_hour_df.head(7), color="#ffd080", ax=ax[0])

# setting grafik 1
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam", fontsize=18)
ax[0].set_title("Jam dengan pengguna rental sepeda terbanyak", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=13)

# mencari record dengan jumlah pengguna tertinggi
max_index = sum_hour_df['total_user'].head(7).idxmax()

# atur warna bar tertinggi menjadi berbeda
ax[0].patches[max_index].set_facecolor('#df9c20')

# format titik pada angka ribuan
ax[0].yaxis.set_major_formatter('{x:,.0f}')

# grafik 2: jam dengan pengguna rental tersedikit
sns.barplot(x="hour", y="total_user", data=sum_hour_df.sort_values(by="total_user", ascending=True).head(7), color="#ffd080", ax=ax[1])

# setting grafik 2
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam",  fontsize=18)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_left()
ax[1].set_title("Jam dengan pengguna rental sepeda tersedikit", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=13)

# mencari record dengan jumlah pengguna terendah
min_index = inversed_sum_hour_df['total_user'].head(7).idxmin()

# atur warna bar tertinggi menjadi berbeda
ax[1].patches[min_index].set_facecolor('#df9c20')

# format titik pada angka ribuan
ax[1].yaxis.set_major_formatter('{x:,.0f}')

# menampilkan plot
plt.suptitle("Jumlah Pengguna Rental Sepeda berdasarkan Jam", fontsize=22, fontweight=600)
st.pyplot(fig)

#4
st.subheader("Jumlah Pengguna Bike Sharing Berdasarkan Cuaca")
# define objek grafik
fig = plt.figure(figsize=(10, 5))

# define data terkait ke grafik batang
ax = sns.barplot(
    y="total_user",
    x="weather",
    data=sum_weather_df,
    color="#ffd080"
)

# mencari record dengan jumlah pengguna tertinggi
max_index = sum_weather_df['total_user'].idxmax()

# atur warna bar tertinggi menjadi berbeda
ax.patches[max_index].set_facecolor('#df9c20')

# format titik pada angka ribuan
ax.yaxis.set_major_formatter('{x:,.0f}')

# pembentukan visual grafik
plt.title("Jumlah Pengguna berdasarkan Cuaca", loc="center", fontsize=18, fontweight=600)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

#5
st.subheader("Jumlah Pengguna Bike Sharing Berdasarkan Temperatur")
# define objek grafik
fig = plt.figure(figsize=(10, 5))

# define data terkait ke grafik batang
ax = sns.barplot(
    y="total_user",
    x="temp_group",
    data=sum_temp_df,
    color="#ffd080"
)

# mencari record dengan jumlah pengguna tertinggi
max_index = sum_temp_df['total_user'].idxmax()

# atur warna bar tertinggi menjadi berbeda
ax.patches[max_index].set_facecolor('#df9c20')

# format titik pada angka ribuan
ax.yaxis.set_major_formatter('{x:,.0f}')

# pembentukan visual grafik
plt.title("Jumlah Pengguna berdasarkan Temperatur", loc="center", fontsize=18, fontweight=600)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.caption('Copyright @ Budy Haryono 2023')