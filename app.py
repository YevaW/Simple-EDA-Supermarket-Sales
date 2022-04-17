import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as scipy
from scipy import stats


st.set_page_config(page_title = 'Supermarket Sales Report',
                  page_icon = "📊",
                  layout = "wide", #wide
                  initial_sidebar_state = "expanded",
                  menu_items = {
                      'About' : ' 3 Months Supermarket Sales Report '
                  })

df = pd.read_csv('supermarket_sales - Sheet1.csv')
df['Date'] = pd.to_datetime (df['Date'])
df['Time'] = pd.to_datetime (df['Time'])
df['Day'] = df['Date'].apply(lambda x: x.day)
df['Month'] = df['Date'].apply(lambda x: x.month)
df['Year'] = df['Date'].apply(lambda x: x.year)
df['Hour'] = df['Time'].apply(lambda x: x.hour)
df ['Minute'] = df['Time'].apply(lambda x: x.minute)
df["week_days"] = df["Date"].dt.day_name()
df['Count'] = 1

page = st.sidebar.selectbox("Apa yang ingin anda ketahui?", ['Sales Overview', 'Detailed Data Graph', 'Hypothesis Testing'])

if page == 'Sales Overview':
    st.title('Overview of Total Sales in 3 Months')

#TOP KPI's:
    total_sales = int(df['Total'].sum())
    avg_rating = round(df['Rating'].mean(), 1)
    star_rating = ":star:" *int(round(avg_rating,0))
    avg_sale_by_trans = round(df['Total'].mean(), 2)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"US $ {total_sales:,}")
    with middle_column:
        st.subheader("Average Rating: ")
        st.subheader(f"{avg_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sales per Transaction:")
        st.subheader(f"US $ {avg_sale_by_trans}")
    
    st.markdown("---")

    st.subheader('Tentang Halaman ini')
    '''Halaman ini menampilkan data-data *overview* dari laporan supermarket selama 3 bulan'''
    '''data yang digunakan merupakan data penjualan supermarket 
    yang terdiri dari 3 cabang supermarket dengan masing-masing cabang di satu wilayah tertentu.'''
    '''Untuk melihat *raw data* klik *check box* berikut:'''
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df)
    
    '''Untuk melihat *overview*, pilih dari *dropbox* berikut:'''

    datas = st.selectbox("Pilih Data Untuk Ditampilkan", ['Sales by City', 'Product Line Sales Distribution', 'Payment Mode', 'Others'])
    if datas == ('Sales by City'):
       st.subheader('City-Wise Sales Distribution')
       pie1= plt.figure(figsize=(5,4))
       piexplode= [0, 0.1, 0]
       piecolors = ["lightslategrey", "crimson", "darkgrey"]
       plt.pie(df.groupby('City')['gross income'].sum(), explode= piexplode, labels=df['City'].unique(), autopct= '%1.1f%%', colors= piecolors, shadow= True)
       st.pyplot(pie1, size = (5,4))
       st.subheader('Penjelasan')
       '''
       Seperti terlihat pada *pie-chart*, diketahui bahwa persebaran penjualan di ketiga kota selama periode 3 bulan ini tidaklah jauh berbeda'''
       '''
       Naypyitaw memiliki persentase penjualan yang sedikit lebih baik dari dua kota lainnya. Tapi tidak cukup signifikan'''

    if datas == ('Product Line Sales Distribution'):
        st.subheader('Total Product Sales Distribution')
        pie2 = plt.figure(figsize = (10,8))
        plt.pie(df.groupby('Product line')['gross income'].sum(),explode= None, labels=df['Product line'].unique(), autopct='%1.1f%%')
        st.pyplot(pie2)
        st.subheader('Penjelasan')
        '''Seperti terlihat pada *pie-chart*, penjualan produk tersebar merata'''
        '''Tidak ada produk yang memiliki penjualan jauh diatas yang lain.'''

    if datas == ('Payment Mode'):
        st.subheader('Payment Mode Used Distribution')
        pie3 = plt.figure(figsize = (10,8))
        plt.pie(df.groupby('Payment')['gross income'].sum(),explode= None, labels=df['Payment'].unique(), autopct='%1.1f%%')
        st.pyplot(pie3)
        st.subheader('Penjelasan')
        '''Ketiga jenis metode pembayaran digunakan secara cukup imbang oleh para pelanggan.'''
    
    elif datas == ('Others'):
        st.subheader('Data Not Found?')
        '''
        Your data is not here. 
        You probably searching a more detailed data, check the Detailed Data Graph page'''




elif page == 'Detailed Data Graph':
    st.title('3 Months Supermarket Data')
    st.subheader('Tentang Halaman ini')
    '''Halaman ini menampilkan data-data mendetail dari laporan supermarket selama 3 bulan di 3 cabang'''

    st.header('Gross Income')
    st.text('Anda dapat menampilkan grafik pendapatan kotor dari kota dan pembeli (baik member maupun non-member).')
    st.markdown('Pilih Data Anda')
    graph1  = st.selectbox("Choose Data to Display", ['Gross Income per Kota', 'Gross Income Member vs Non-Member',
    'Gross Income by Gender', 'Gross Income by Gender Member - Non Member', 'Others'])
    
    if graph1 == ('Gross Income per Kota'):
        st.subheader('Average Gross Income per Kota')
        fig1,ax1 = plt.subplots()

        palette1 = ['indianred', 'lightcoral', 'rosybrown']

        df.groupby('City').sum()['gross income'].sort_values(ascending=False).plot(kind='bar',ax=ax1, color = palette1)

        ax1.set_title('Rata rata Gross Income Tiap kota') 
        ax1.set_xlabel('Kota') 
        ax1.set_ylabel('gross income') 
        st.pyplot(fig1)
        st.subheader('Penjelasan')
        '''Dari ketiga kota, tidak terlihat perbedaan pendapatan kotor yang signifikan.'''
        '''Pendapatan Naypyitaw *sedikit lebih baik* dari dua kota lainnya, tapi itu pun tidak signifikan'''
    
    if graph1 == ('Gross Income Member vs Non-Member'):
        fig2,ax2 = plt.subplots()
        palette2 = ['salmon', 'maroon']

        df.groupby('Customer type').sum()['gross income'].sort_values(ascending=False).plot(kind='bar',ax=ax2, color=palette2)

        ax2.set_title('Gross Income tiap tipe konsumen') 
        ax2.set_xlabel('Customer type') 
        ax2.set_ylabel('gross_income') 
        st.pyplot(fig2)
        st.subheader('Penjelasan')
        '''Dari dua jenis pelanggan, member dan non-member, tidak terlihat perbedaan pendapatan kotor yang signifikan.'''
    
    if  graph1 == ('Gross Income by Gender'):
        st.subheader('Avrage Gross Income per Gender')
        fig3,ax3 = plt.subplots()
        palette3 = ['lightsalmon', 'cornflowerblue']
        df.groupby('Gender').sum()['gross income'].sort_values(ascending=False).plot(kind='bar',ax=ax3, color = palette3)

        ax3.set_title('Gross Income berdasarkan gender') 
        ax3.set_xlabel('Gender') 
        ax3.set_ylabel('gross income')
        st.pyplot(fig3)
        st.subheader('Penjelasan')
        '''Berdasarkan gender, terlihat perbedaan pendapatan kotor bahwa perempuan sedikit lebih tinggi dari laki-laki.'''
        '''Tetapi angka perbedaannya terlihat tidak terlalu jauh'''
    
    if  graph1 == ('Gross Income by Gender Member - Non Member'):
        fig4= plt.figure(figsize=(10,4))
        palette3 = ['lightsalmon', 'cornflowerblue']
        sns.barplot(data = df, x = 'Customer type' , y =  'gross income' , hue = 'Gender', palette = palette3).set(title='Income per Gender per Type')
        plt.yticks(list(range(0 , 20 , 5))) # Changing Y axis value for a better reading
        st.pyplot(fig4)
        st.subheader('Penjelasan')
        '''Dari grafik, terlihat bahwa meskipun terdapat perbedaan, namun tidak terlalu jauh pendapatan kotor antara member perempuan & laki-laki
        dan non-member perempuan & laki-laki'''

    st.header('Sales')
    st.text('Anda dapat menampilkan grafik penjualan dari Supermarket')
    st.markdown('Pilih Data Anda')
    graph2  = st.selectbox("Choose Data to Display", ['Monthly Sales per Branch', 
    'Daily Sales per Branch','Product Sales per Gender'])

    if graph2 == ('Monthly Sales per Branch'):
        fig5= plt.figure(figsize=(10,4))
        palette1 = ['indianred', 'lightcoral', 'rosybrown']
        sns.barplot(data = df, x = 'Month' ,y =  'Total' , hue = 'City', palette = palette1, saturation = 5, errcolor = 'lightblue').set(title='Sales per Branch per Month')
        plt.yticks(list(range(0 , 550 , 50))) # Changing Y axis value for a better reading
        st.pyplot(fig5)
        st.subheader('Penjelasan')
        '''Terlihat bahwa penjualan perbulan dari tiap cabang cukup seimbang'''
    
    if graph2 == ('Daily Sales per Branch'):
        # Creating a list to sort the days of the week on specific order
        orderList = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        fig6= plt.figure(figsize=(10,4))
        palette1 = ['indianred', 'lightcoral', 'rosybrown']
        sns.boxplot(data = df, x = 'week_days', y = 'Total', hue = 'City', palette = palette1, order= orderList).set(title='Total sales per days of the week per Branch')
        plt.yticks(list(range(0 , 1100 , 100))) # Changing Y axis value for a better reading
        st.pyplot(fig6)
        st.subheader('Penjelasan')
        '''Terlihat bahwa penjualan harian dari tiap cabang, meskipun terdapat hari-hari dimana penjualan lebih banyak,
        tapi secara keseluruhan cukup seimbang'''
    
    if graph2 == ('Product Sales per Gender'):
        fig7= plt.figure(figsize=(10,4))
        palette3 = ['lightsalmon', 'cornflowerblue']
        sns.barplot(data = df, x = 'City' , y =  'Day' , hue = 'Gender', palette = palette3).set(title='Total Sales per product type per Gender')
        st.pyplot(fig7)
        st.subheader('Penjelasan')
        '''Dari grafik penjualan, meskipun tidak terlalu jauh, terlihat bahwa penjualan lebih banyak kepada 
        pelanggan laki-laki'''
    
    st.header('Payment Method')
    st.text('Anda dapat menampilkan grafik persebaran dari metode pembayaran yang digunakan oleh pembeli di supermarket')
    st.markdown('Pilih Data Anda')
    graph3  = st.selectbox("Choose Data to Display", ['Payment Method per Branch', 
    'Payment Method per Product'])

    if graph3 == ('Payment Method per Branch'):
        palette4 = ['gold', 'khaki', 'goldenrod']
        fig8 = plt.figure(figsize = (15,8))
        sns.boxplot('Product line','Total','Payment',data = df, palette = palette4)
        st.pyplot(fig8)
        st.subheader('Penjelasan')
        '''Metode pembayaran yang digunakan di tiap cabang, terdistribusi merata. 
        Tidak ada metode pembayaran yang lebih banyak digunakan secara signifikan'''

    if graph3==('Payment Method per Product'):
        palette4 = ['gold', 'khaki', 'goldenrod']
        fig9=plt.figure(figsize = (15,8))
        sns.boxplot('Branch','Total','Payment',data = df, palette = palette4)
        st.pyplot(fig9)
        st.subheader('Penjelasan')
        '''Metode pembayaran yang digunakan untuk transaksi tiap produk, terdistribusi merata. 
        Tidak ada metode pembayaran yang lebih banyak digunakan secara signifikan'''

    elif st.checkbox('Others'):
        st.subheader('Data Not Found?')
        st.write('Your data is not here. Check Sales Overview or Hypothesis Testing')

else:
    st.title('Hypothesis Testing')
    Member = df[df['Customer type']=='Member'][['Invoice ID','gross income']].groupby('Invoice ID').sum()
    non = df[df['Customer type']=='Normal'][['Invoice ID','gross income']].groupby('Invoice ID').sum()
    t_stat, p_val = stats.ttest_ind(Member,non)

    '''Pada Hypothesis Testing ini akan digunakan metode P-Value Testing untuk *Two-Tailed Test*. 
    Yang mana, hypothesis testing ini menguji apakah rata-rata penghasilan kotor dari pelanggan member sama dengan pelanggan non-member'''

    '''Hipotesis yang akan di uji adalah sebagai berikut :'''
    '''1. H0: μ Gross income Member = μ Gross income Non- Member: *rata-rata pendapatan kotor Member sama dengan Non-Member*'''
    '''2. H1: μ Gross income Member != μ Gross income Non- Member: *rata-rata pendapatan kotor Member tidak sama dengan Non-Member*'''
    

    '''Berikut adalah data rata-rata penghasilan kotor:'''
    if st.button('Tunjukkan Data'):
        st.write(('Rata-rata penghasilan kotor dari Konsumen dengan status member: {}'.format(np.round(Member['gross income'].mean()))), ('Rata-rata penghasilan kotor dari Konsumen dengan status non-member: {}'.format(np.round(non['gross income'].mean()))))
    elif st.button('Sembunyikan Data'):
        st.write('Anda dalam Mode Sembunyikan Data.')

    '''Untuk mendapatkan gambaran pendapatan kotor dari member dan non-member, anda bisa memilih untuk menampilkan grafik pada kotak dibawah:'''
    members = st.selectbox("Pilih Grafik Anda", ['Pendapatan Member dan Non-Member', 'Pendapatan Member dan Non-Member sesuai Gender'])
    if members == 'Pendapatan Member dan Non-Member':
        member1, ax2 = plt.subplots()
        palette2 = ['salmon', 'maroon']

        df.groupby('Customer type').sum()['gross income'].sort_values(ascending=False).plot(kind='bar',ax=ax2, color=palette2)

        ax2.set_title('Gross Income tiap tipe konsumen') 
        ax2.set_xlabel('Customer type') 
        ax2.set_ylabel('gross_income') 
        st.pyplot(member1)

    if members == 'Pendapatan Member dan Non-Member sesuai Gender':
        member2= plt.figure(figsize=(10,4))
        palette3 = ['lightsalmon', 'cornflowerblue']
        sns.barplot(data = df, x = 'Customer type' , y =  'gross income' , hue = 'Gender', palette = palette3).set(title='Income per Gender per Type')
        plt.yticks(list(range(0 , 20 , 5))) # Changing Y axis value for a better reading
        st.pyplot(member2)

    '''Pengetesan menggunakan kalkulasi P-Value dan T-Stat yang nilainya dapat dilihat sebagai berikut:'''
    testval = st.radio("Pilih nilai yang akan ditampilkan", ('P-Val', 'T-Stat'))
    if testval == 'P-Val':
        st.write('P-value:',p_val)
        '''p_value [0.53439496] bernilai lebih besar dibandingkan dengan critical value = 0.05, yang berarti H0 diterima. '''
        '''ini berarti bahwa rata-rata pendapatan kotor Pelanggan yang merupakan Member sama dengan rata-rata pendapatan kotor Pelanggan yang bukan member.'''
    if testval == 'T-Stat':
        st.write('t-statistics:',t_stat)
   


    '''Berikut ini adalah tampilan dari grafik gaussian distribution terhadap uji hipotesis yang telah dilaksanakan:'''
    Memb_pop = np.random.normal(Member['gross income'].mean(), Member['gross income'].std(),500)
    biasa_pop = np.random.normal(non['gross income'].mean(), non['gross income'].std(),500)

    ci = stats.norm.interval(0.95,Member['gross income'].mean(), Member['gross income'].std())
    hypo= plt.figure(figsize=(16,5))
    sns.distplot(Memb_pop, label='Rata-rata gross income member *Pop',color='blue')
    sns.distplot(biasa_pop, label='Rata-rata gross income non member *Pop',color='red')


    plt.axvline(Member['gross income'].mean(), color='blue', linewidth=2, label='Member mean')
    plt.axvline(non['gross income'].mean(), color='red',  linewidth=2, label='Non mean')


    plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
    plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2)

    plt.axvline(Memb_pop.mean()+t_stat[0]*Memb_pop.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
    plt.axvline(Memb_pop.mean()-t_stat[0]*Memb_pop.std(), color='black', linestyle='dashed', linewidth=2)

    plt.legend()
    st.pyplot(hypo)