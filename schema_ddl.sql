--customer profiles ddl
CREATE TABLE customer_profiles (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT CHECK (age BETWEEN 18 AND 70),
    income NUMERIC(10, 2) CHECK (income BETWEEN 30000 AND 150000),
    mobile VARCHAR(15) NOT NULL UNIQUE,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    education VARCHAR(50) CHECK (education IN ('High School', 'Bachelor', 'Master', 'PhD')),
    occupation VARCHAR(255),
    zip_code INT CHECK (zip_code BETWEEN 10000 AND 99999)
);

--purchase history ddl 
CREATE TABLE purchase_history (
    purchase_id SERIAL PRIMARY KEY,
    mobile VARCHAR(15) NOT NULL REFERENCES customer_profiles(mobile),
    date DATE NOT NULL,
    amount NUMERIC(10, 2) CHECK (amount BETWEEN 20 AND 50000),
    store VARCHAR(50) CHECK (store IN ('Store_A', 'Store_B', 'Store_C', 'Store_D')),
    payment_method VARCHAR(50) CHECK (payment_method IN ('Credit Card', 'Debit Card', 'Cash', 'Digital Wallet')),
    product_category VARCHAR(50) CHECK (product_category IN ('Electronics', 'Clothing', 'Groceries', 'Books')),
    quantity INT CHECK (quantity BETWEEN 1 AND 500)
);


--loading file into db using copy command

COPY customer_profiles(name, age, income, mobile, gender, education, occupation, zip_code)
FROM '/path/to/your/customer_profiles.csv'
DELIMITER ','
CSV HEADER;


-- loading json into db usig copy commmand


COPY purchase_history(mobile, date, amount, store, payment_method, product_category, quantity)
FROM PROGRAM 'cat /path/to/your/purchase_history.json | jq -c ".[]"'
WITH (FORMAT csv);
