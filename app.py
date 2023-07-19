import pandas as pd

def read_purchase_data(file_path):
    return pd.read_csv(file_path)

def get_num_of_players(data_frame):
    return data_frame['SN'].nunique()

def create_summary_data_frame(data_frame):
    average_price = data_frame['Price'].mean()
    unique_items_count = data_frame['Item Name'].nunique()
    return pd.DataFrame({
        'average price': [average_price],
        'number of unique items': [unique_items_count]
    })

def calculate_gender_demographics(data_frame):
    gender_counts = data_frame['Gender'].value_counts()
    total_gender_count = gender_counts.sum()
    percentage_of_players = gender_counts.div(total_gender_count) * 100
    return pd.DataFrame({
        'total count': gender_counts,
        'percentage of players': percentage_of_players
    }).sort_index()

def calculate_age_demographics(data_frame, bins, labels, num_of_players):
    age_group_counts = data_frame.drop_duplicates(subset='SN').groupby(
        pd.cut(data_frame['Age'], bins=bins, labels=labels)
    )['SN'].size().reset_index(name='Total_Count')
    age_group_counts['Percentage_of_Players'] = age_group_counts['Total_Count'] / num_of_players * 100
    return age_group_counts.copy()

def perform_gender_purchasing_analysis(data_frame):
    return data_frame.groupby('Gender').agg(
        purchase_count=('SN', 'count'),
        average_purchase_price=('Price', 'mean'),
        average_purchase_total_per_person=('Price', lambda x: x.sum() / num_of_players)
    )

def perform_age_purchasing_analysis(data_frame, bins, labels, num_of_players):
    return data_frame.groupby(
        pd.cut(data_frame['Age'], bins=bins, labels=labels)
    ).agg(
        purchase_count=('SN', 'count'),
        average_purchase_price=('Price', 'mean'),
        average_purchase_total_per_person=('Price', lambda x: x.sum() / num_of_players)
    )

def calculate_top_spenders(data_frame):
    return data_frame.groupby('SN').agg(
        purchase_count=('Item ID', 'count'),
        total_purchases=('Price', 'sum'),
        average_purchase_price=('Price', 'mean')
    ).sort_values('total_purchases', ascending=False)

def calculate_most_popular_items(data_frame):
    return data_frame.groupby(['Item ID', 'Item Name']).agg(
        purchase_count=('SN', 'count'),
        total_purchase_value=('Price', 'sum'),
        average_purchase_price=('Price', 'mean')
    ).sort_values('purchase_count', ascending=False)

def calculate_most_profitable_items(data_frame):
    return data_frame.sort_values('total_purchase_value', ascending=False)


# Read Purchasing File and store into Pandas DataFrame
purchase_data = read_purchase_data("Resources/purchase_data.csv")

# Player Count
num_of_players = get_num_of_players(purchase_data)

# Summary Data Frame
summary_data_frame = create_summary_data_frame(purchase_data)

# Gender Demographics
gender_data = calculate_gender_demographics(purchase_data)

# Age Demographics
bins = list(range(0, 101, 5))
labels = ['less than 10'] + [f'{i} - {i + 4}' for i in range(10, 45, 5)]
age_demographics = calculate_age_demographics(purchase_data, bins, labels, num_of_players)

# Purchasing Analysis (Gender)
gender_purchasing_analysis_df = perform_gender_purchasing_analysis(purchase_data)

# Purchasing Analysis (Age)
age_purchasing_demo = perform_age_purchasing_analysis(purchase_data, bins, labels, num_of_players)

# Top Spenders
top_spenders = calculate_top_spenders(purchase_data)

# Most Popular Items
most_popular_items = calculate_most_popular_items(purchase_data)

# Most Profitable Items
most_profitable_items = calculate_most_profitable_items(most_popular_items)
