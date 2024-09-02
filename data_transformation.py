from prefect import flow, task
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import random
import json
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from faker import Faker
import os
from flask import Flask, jsonify
import json
import random
import json
import pandas as pd
from flask import Flask, jsonify
import requests
import threading


# Example function to generate customer profiles
@task
def generate_customer_profiles(num_customers):

    profiles = []
    fake = Faker()

    # Generate unique first and last names
    first_names = [fake.first_name() for _ in range(5000)]
    last_names = [fake.last_name() for _ in range(5000)]

    # Create unique name combinations
    names = list(set([f"{first} {last}" for first in first_names for last in last_names]))
    random.shuffle(names)  # Shuffle to ensure randomness

    # Generate a diverse set of occupations
    occupations = [
        "Software Engineer", "Data Scientist", "Doctor", "Teacher", "Artist", "Entrepreneur", "Chef",
        "Pilot", "Architect", "Nurse", "Journalist", "Photographer", "Designer", "Musician",
        "Actor", "Author", "Librarian", "Engineer", "Accountant", "Banker", "Consultant", "Dentist",
        "Pharmacist", "Veterinarian", "Lawyer", "Judge", "Electrician", "Plumber", "Mechanic", 
        "Carpenter", "Welder", "Blacksmith", "Biologist", "Chemist", "Physicist", "Geologist", 
        "Astronomer", "Mathematician", "Statistician", "Economist", "Sociologist", "Anthropologist",
        "Historian", "Philosopher", "Psychologist", "Therapist", "Social Worker", "Politician", 
        "Diplomat", "Clergy", "Rabbi", "Imam", "Priest", "Pastor", "Minister", "Military Officer", 
        "Firefighter", "Police Officer", "Paramedic", "Surgeon", "Radiologist", "Pathologist", 
        "Anesthesiologist", "Gastroenterologist", "Pediatrician", "Dermatologist", "Neurologist", 
        "Psychiatrist", "Oncologist", "Orthopedic Surgeon", "Urologist", "Pulmonologist", 
        "Endocrinologist", "Nephrologist", "Rheumatologist", "Infectious Disease Specialist", 
        "Cardiologist", "Geriatrician", "Obstetrician", "Gynecologist", "Radiation Therapist", 
        "Occupational Therapist", "Physical Therapist", "Speech Therapist", "Respiratory Therapist",
        "Chiropractor", "Optometrist", "Podiatrist", "Dentist", "Orthodontist", "Periodontist",
        "Prosthodontist", "Oral Surgeon", "Endodontist", "Pediatric Dentist", "Veterinarian", 
        "Animal Trainer", "Zookeeper", "Agricultural Scientist", "Farmer", "Fisherman", "Rancher",
        "Forester", "Park Ranger", "Environmentalist", "Urban Planner", "Landscape Architect"
    ]

    
    for i in range(num_customers):
        profile = {
            'name': random.choice(names),
            'age': random.randint(18, 70),
            'income': round(random.uniform(30000, 150000), 2),
            'mobile': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'gender': random.choice(['Male', 'Female']),
            'education': random.choice(['High School', 'Bachelor', 'Master', 'PhD']),
            'occupation': random.choice(occupations),
            'zip_code': random.randint(10000, 99999)
        }
        profiles.append(profile)

    df_profiles = pd.DataFrame(profiles)
    df_profiles.to_csv('customer_profiles.csv', index=False)
    return df_profiles



@task
def generate_purchase_history(num_records):
    history = []
    stores = ['Store_A', 'Store_B', 'Store_C', 'Store_D']

    # Load customer profiles to get existing mobile numbers
    df_profiles = pd.read_csv('customer_profiles.csv')
    existing_mobiles = df_profiles['mobile'].tolist()
    
    for i in range(num_records):
        record = {
            'mobile': random.choice(existing_mobiles),
            'date': pd.Timestamp(random.randint(1609459200, 1672444800), unit='s').strftime('%Y-%m-%d'),
            'amount': round(random.uniform(20, 50000), 2),
            'store': random.choice(stores),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet']),
            'product_category': random.choice(['Electronics', 'Clothing', 'Groceries', 'Books']),
            'quantity': random.randint(1, 500)
        }
        history.append(record)

    with open('purchase_history.json', 'w') as f:
        json.dump(history, f)
    return history



@task
def start_mock_api(json_file='purchase_history.json'):
    """
    Prefect task to start a mock API server that serves the purchase history data.
    
    Args:
        json_file (str): Path to the JSON file containing purchase history data.
    """
    app = Flask(__name__)

    # Load the JSON data from the file
    with open(json_file, 'r') as f:
        purchase_history = json.load(f)

    # Create an API endpoint to serve the data
    @app.route('/api/purchase_history', methods=['GET'])
    def get_purchase_history():
        return jsonify(purchase_history)

    # Run the Flask app in a separate thread to not block the flow
    def run_app():
        app.run(debug=False, use_reloader=False)

    thread = threading.Thread(target=run_app)
    thread.daemon = True
    thread.start()

@task
def consume_api(api_url='http://127.0.0.1:5000/api/purchase_history'):
    """
    Prefect task to consume data from the mock API.
    
    Args:
        api_url (str): The URL of the API endpoint.
    
    Returns:
        list: The data retrieved from the API.
    """
    response = requests.get(api_url)
    data = response.json()
    return data

@task
def extract_data(data):
    customer_profiles = pd.read_csv('customer_profiles.csv')
    purchase_history = pd.DataFrame(data)

    # Perform a left join to keep all customer profiles
    data = pd.merge(customer_profiles, purchase_history, on='mobile', how='left')

    # Fill missing data with default values
    data.fillna({
        'amount': random.randint(0, 1000),
        'quantity': random.randint(0, 1000),
        'date': pd.Timestamp('today').strftime('%Y-%m-%d'),
        'store': 'Unknown',
        'payment_method': 'Unknown',
        'product_category': 'Unknown'
    }, inplace=True)

    return data



@task
def clean_data(df):
    df.drop_duplicates(inplace=True)
    df['age'].fillna(df['age'].median(), inplace=True)
    df['income'].fillna(df['income'].median(), inplace=True)
    df['amount'].fillna(df['income'].median(), inplace=True)
    df['quantity'].fillna(df['quantity'].median(), inplace=True)
    df['age'] = df['age'].apply(lambda x: 99 if x > 99 else x)
    df['product_category'] = df['product_category'].replace({'Electornics': 'Electronics'})
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['zip_code'] = df['zip_code'].astype(str)
    
    return df


@task
def calculate_clv(df):
    clv = df.groupby('mobile')['amount'].sum().reset_index()
    clv.columns = ['mobile', 'CLV']
    df = pd.merge(df, clv, on='mobile', how='left')
    return df


@task
def feature_engineering(df):
    loyalty = df.groupby('mobile').size().reset_index(name='num_purchases')
    df['date'] = pd.to_datetime(df['date'])
    frequency = df.groupby('mobile')['date'].apply(lambda x: (x.max() - x.min()).days / max(1, len(x))).reset_index(name='avg_purchase_frequency')
    df['spending_score'] = df['income'] / df['CLV']
    df = pd.merge(df, loyalty, on='mobile', how='left')
    df = pd.merge(df, frequency, on='mobile', how='left')
    return df


@task
def normalize_and_impute_data(df):
    df.replace([float('inf'), float('-inf')], float('nan'), inplace=True)
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    columns_with_all_nan = df[numeric_columns].columns[df[numeric_columns].isnull().all()]
    df = df.drop(columns=columns_with_all_nan)
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='median')
    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
    scaler = MinMaxScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    df['gender'] = LabelEncoder().fit_transform(df['gender'])
    df['education'] = LabelEncoder().fit_transform(df['education'])
    df['occupation'] = LabelEncoder().fit_transform(df['occupation'])
    df['product_category'] = LabelEncoder().fit_transform(df['product_category'])
    
    return df






@task
def segment_customers(df, min_clusters=2, max_clusters=15, plot_file_path="silhouette_scores.png", cluster_plot_dir="cluster_plots"):
    required_columns = ['age', 'income', 'CLV', 'num_purchases', 'avg_purchase_frequency', 'spending_score']
    features = df[required_columns]
    
    silhouette_scores = []
    best_n_clusters = min_clusters
    best_score = -1
    
    # Loop over a range of possible cluster numbers
    for n_clusters in range(min_clusters, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(features)
        silhouette_avg = silhouette_score(features, cluster_labels)
        silhouette_scores.append(silhouette_avg)
        
        # Update the best score and corresponding number of clusters
        if silhouette_avg > best_score:
            best_score = silhouette_avg
            best_n_clusters = n_clusters
    
    # Plot the silhouette scores to visualize
    plt.figure(figsize=(10, 6))
    plt.plot(range(min_clusters, max_clusters + 1), silhouette_scores, marker='o')
    plt.title("Silhouette Scores for KMeans Clustering")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Score")
    plt.grid(True)
    
    # Save the silhouette score plot
    plt.savefig(plot_file_path)
    plt.close()
    
    # Fit KMeans with the optimal number of clusters
    final_kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
    df['segment'] = final_kmeans.fit_predict(features)
    
    # Create directory for individual cluster plots
    os.makedirs(cluster_plot_dir, exist_ok=True)
    
    # Plot and save each cluster separately
    for cluster in range(best_n_clusters):
        cluster_data = df[df['segment'] == cluster]
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        scatter = ax.scatter(
            cluster_data['income'], cluster_data['CLV'], cluster_data['age'], 
            c=cluster_data['segment'], cmap='viridis', s=50, alpha=0.7
        )
        ax.set_title(f'Cluster {cluster} (n_clusters={best_n_clusters})')
        ax.set_xlabel('Income')
        ax.set_ylabel('Customer Lifetime Value (CLV)')
        ax.set_zlabel('Age')
        
        # Save the individual cluster plot
        cluster_plot_path = os.path.join(cluster_plot_dir, f"cluster_{cluster}.png")
        plt.savefig(cluster_plot_path)
        plt.close()
    
    print(f"Optimal number of clusters: {best_n_clusters}")
    print(f"Silhouette scores plot saved as {plot_file_path}")
    print(f"Individual cluster plots saved in directory: {cluster_plot_dir}")
    return df

@task
def aggregate_metrics(df):
    metrics = df.groupby('segment').agg(
        avg_age=('age', 'mean'),
        avg_income=('income', 'mean'),
        total_CLV=('CLV', 'sum'),
        avg_num_purchases=('num_purchases', 'mean'),
        avg_spending_score=('spending_score', 'mean')
    ).reset_index()
    
    # Adding some noise to the results to make them more realistic
    metrics['avg_age'] = metrics['avg_age'] + random.uniform(-5, 5)
    metrics['avg_income'] = metrics['avg_income'] * random.uniform(0.8, 1.2)
    metrics['total_CLV'] = metrics['total_CLV'] * random.uniform(0.9, 1.1)
    metrics['avg_num_purchases'] = metrics['avg_num_purchases'] * random.uniform(0.85, 1.15)
    metrics['avg_spending_score'] = metrics['avg_spending_score'] * random.uniform(0.9, 1.1)
    
    return metrics



@flow
def customer_segmentation_pipeline():
    profiles = generate_customer_profiles(100)
    history = generate_purchase_history(200)
    # Start mock API server
    start_mock_api()
    # Consume the API
    data = consume_api()
    data_extract= extract_data(data)
    cleaned_data = clean_data(data_extract)
    data_with_clv = calculate_clv(cleaned_data)
    data_with_features = feature_engineering(data_with_clv)
    normalized_data = normalize_and_impute_data(data_with_features)
    segmented_data = segment_customers(normalized_data)
    metrics = aggregate_metrics(segmented_data)
    
    print(metrics)

# Run the flow
if __name__ == "__main__":
    customer_segmentation_pipeline()
