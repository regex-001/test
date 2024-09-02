
# Customer Segmentation ETL Pipeline

Welcome! This repository contains an ETL pipeline project designed to help an e-commerce company better understand its customers. The main goal here is to segment customers based on their behavior, demographics, and purchase history so that the company can create more targeted and effective marketing campaigns.

## What’s This About?

In the competitive world of e-commerce, knowing your customers is crucial. This project addresses the challenge of customer segmentation, which is all about grouping customers who share similar characteristics. By doing this, businesses can tailor their marketing efforts, improve customer experiences, and ultimately drive sales.

## How Does It Work?

This project provides a flexible ETL (Extract, Transform, Load) pipeline that processes customer data, cleans it up, creates new features, and uses machine learning to segment customers into meaningful groups. The final results are stored in a database, ready for further analysis.

## Key Features

- **Data Extraction:** Simulates pulling data from a REST API and other sources.
- **Data Cleaning:** Takes care of missing values, duplicates, outliers, and other common issues.
- **Feature Engineering:** Creates useful features like Customer Lifetime Value (CLV), customer loyalty, purchase frequency, and spending scores.
- **Customer Segmentation:** Uses K-means clustering to group customers based on their profiles.
- **Data Loading:** Saves everything into a reporting database that’s easy to work with.

## Getting Started

### Prerequisites

You’ll need Python 3.8 or later to run this project. Make sure you have the following Python packages installed:

- `pandas`
- `numpy`
- `scikit-learn`
- `requests`
- `sqlite3` (comes with Python, so you’re good here)

To make things easy, all the necessary packages are listed in the `requirements.txt` file.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/customer-segmentation-etl.git
   cd customer-segmentation-etl
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the ETL pipeline:**

   Simply run the main script to kick off the pipeline:

   ```bash
   python etl_pipeline.py
   ```

## Project Layout

Here’s a quick rundown of what you’ll find in this project:

```
customer-segmentation-etl/
│
├── data/
│   ├── customer_profiles.csv       # Generated customer profile data
│   └── purchase_history.json       # Generated purchase history data
│
├── etl_pipeline.py                 # Main ETL pipeline script
├── requirements.txt                # Python dependencies
└── README.md                       # This very file you're reading
```

## How the Pipeline Works

1. **Data Generation:**
   - **Customer Profiles:** Generates sample customer data like name, age, income, gender, etc.
   - **Purchase History:** Simulates customer purchase data and stores it in a JSON file to mimic a REST API response.

2. **Data Extraction:**
   - Reads customer profiles from a CSV file.
   - Simulates a REST API call by reading purchase history from the JSON file.

3. **Data Cleaning:**
   - Removes duplicates, fills in missing values, corrects any outliers, and makes sure everything is consistent.

4. **Feature Engineering:**
   - Calculates useful metrics like Customer Lifetime Value (CLV) and creates new features like customer loyalty and spending score.

5. **Normalization and Encoding:**
   - Scales numerical features and encodes categorical ones to make them machine-readable.

6. **Customer Segmentation:**
   - Uses the K-means algorithm to cluster customers into different segments based on their profiles.

7. **Data Loading:**
   - Saves the cleaned and segmented data into a SQLite database for easy reporting.

## Database Schema

Once the pipeline runs, the data is saved in a SQLite database with the following structure:

- **`customer_segments`**: Stores detailed customer information along with the segment they belong to.
- **`segment_metrics`**: Aggregates key metrics for each customer segment (e.g., total spend, average CLV).

### Example SQL Schema

```sql
CREATE TABLE customer_segments (
    mobile VARCHAR PRIMARY KEY,
    name VARCHAR,
    age FLOAT,
    income FLOAT,
    gender INT,
    education INT,
    occupation INT,
    zip_code VARCHAR,
    CLV FLOAT,
    num_purchases INT,
    avg_purchase_frequency FLOAT,
    spending_score FLOAT,
    segment INT
);

CREATE TABLE segment_metrics (
    segment INT PRIMARY KEY,
    total_spend FLOAT,
    num_customers INT,
    avg_CLV FLOAT,
    avg_purchases FLOAT,
    avg_spending_score FLOAT
);
```

## Simulating a REST API

In a real-world scenario, you’d probably be pulling data from a live API. In this project, we simulate that by reading from a JSON file (`purchase_history.json`). It’s not the real thing, but it’s a close enough stand-in for this exercise.

## Testing and Validation

After you run the pipeline, you can check the `reporting.db` SQLite database to see how well everything worked:

- Are the customers correctly segmented?
- Do the metrics like total spend and average CLV make sense?
- Is the data clean and consistent?


## Wrap-Up

This project is all about making sense of customer data so businesses can market more effectively. The ETL pipeline is built to be flexible, easy to extend, and ready for real-world applications.

---

*Feel free to contribute, open issues, or just say hello!*
