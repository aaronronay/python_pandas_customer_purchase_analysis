import pandas as pd

# Read Purchasing File and store into Pandas DataFrame
purchase_data = pd.read_csv("Resources/purchase_data.csv")

# Player Count
num_of_players = purchase_data['SN'].nunique()

# Purchasing Analysis (Total)
summary_data_frame = pd.DataFrame({
    'average price': purchase_data['Price'].mean(),
    'number of unique items': purchase_data['Item Name'].nunique()
}, index=[0])

# Gender Demographics
gender_data = pd.DataFrame({
    'percentage of players': purchase_data['Gender'].value_counts(normalize=True) * 100,
    'total count': purchase_data['Gender'].value_counts()
})

# Purchasing Analysis (Gender)
gender_purchasing_analysis_df = purchase_data.groupby('Gender').agg({
    'SN': 'count',
    'Price': ['mean', lambda x: x.sum() / num_of_players]
})
gender_purchasing_analysis_df.columns = ['purchase count', 'average purchase price', 'average purchase total per person']

# Age Demographics
bins = [0, 10, 15, 20, 25, 30, 35, 40, 200]
labels = ['less than 10', '10 - 14', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', 'greater than 40']
purchase_data['age range'] = pd.cut(purchase_data['Age'], bins=bins, labels=labels)
age_demographics = purchase_data.drop_duplicates(subset='SN').groupby('age range').size().reset_index(name='total count')
age_demographics['percentage of players'] = age_demographics['total count'] / num_of_players * 100

# Purchasing Analysis (Age)
age_purchasing_demo = purchase_data.groupby('age range').agg({
    'SN': 'count',
    'Price': ['mean', lambda x: x.sum() / num_of_players]
})
age_purchasing_demo.columns = ['purchase count', 'average purchase price', 'average purchase total per person']

# Top Spenders
top_spenders = purchase_data.groupby('SN').agg({
    'Item ID': 'count',
    'Price': ['sum', 'mean']
})
top_spenders.columns = ['purchase count', 'total purchases', 'average purchase price']
top_spenders = top_spenders.sort_values('total purchases', ascending=False)

# Most Popular Items
most_popular_items = purchase_data.groupby(['Item ID', 'Item Name']).agg({
    'SN': 'count',
    'Price': ['sum', 'mean']
})
most_popular_items.columns = ['purchase count', 'total purchase value', 'average purchase price']
most_popular_items = most_popular_items.sort_values('purchase count', ascending=False)

# Most Profitable Items
most_profitable_items = most_popular_items.sort_values('total purchase value', ascending=False)
