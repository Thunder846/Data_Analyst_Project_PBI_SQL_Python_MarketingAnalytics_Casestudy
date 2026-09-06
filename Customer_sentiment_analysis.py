```python
# ============================================================
# CUSTOMER REVIEW SENTIMENT ANALYSIS
# ============================================================
# Purpose:
# Extract customer reviews from SQL Server, analyze the
# review text using VADER sentiment analysis, combine the
# sentiment with customer ratings, and export the results.


# -------------------- 1. DOWNLOAD VADER --------------------
# Download the VADER lexicon required for sentiment analysis.
nltk.download('vader_lexicon')


# -------------------- 2. FETCH DATA FROM SQL ----------------
# Create a function to connect Python to SQL Server and
# retrieve customer review data using a SQL query.

def fetch_data_from_sql():

    # Connection string contains the SQL Server, database,
    # driver, and authentication details.
    conn_str = (
        "Driver={SQL Server};"
        "Server=ALI-LT2024\\SQLEXPRESS;"
        "Database=PortfolioProject_MarketingAnalytics;"
        "Trusted_Connection=yes;"
    )

    # Establish connection between Python and SQL Server.
    conn = pyodbc.connect(conn_str)

    # SQL query to select the required customer review columns.
    query = """
    SELECT ReviewID, CustomerID, ProductID, ReviewDate,
           Rating, ReviewText
    FROM fact_customer_reviews
    """

    # Execute the SQL query and load the result into
    # a Pandas DataFrame.
    df = pd.read_sql(query, conn)

    # Close the database connection after retrieving the data.
    conn.close()

    # Return the DataFrame.
    return df


# -------------------- 3. LOAD CUSTOMER REVIEWS --------------
# Call the function to retrieve customer reviews from SQL.
customer_reviews_df = fetch_data_from_sql()


# -------------------- 4. INITIALIZE VADER -------------------
# Create the VADER sentiment analyzer.
# VADER is used to determine the sentiment of review text.
sia = SentimentIntensityAnalyzer()


# -------------------- 5. CALCULATE SENTIMENT ----------------
# Create a function that takes a customer review as input
# and returns its VADER compound sentiment score.

def calculate_sentiment(review):

    # polarity_scores() calculates positive, negative,
    # neutral, and compound sentiment scores.
    sentiment = sia.polarity_scores(review)

    # Return only the compound score (-1 to +1).
    return sentiment['compound']


# -------------------- 6. CATEGORIZE SENTIMENT ---------------
# Create a function that combines the sentiment score
# with the customer's numerical rating.
#
# This helps identify situations where the review text
# and star rating do not agree.

def categorize_sentiment(score, rating):

    # Positive text sentiment
    if score > 0.05:

        if rating >= 4:
            return 'Positive'

        elif rating == 3:
            return 'Mixed Positive'

        else:
            return 'Mixed Negative'

    # Negative text sentiment
    elif score < -0.05:

        if rating <= 2:
            return 'Negative'

        elif rating == 3:
            return 'Mixed Negative'

        else:
            return 'Mixed Positive'

    # Neutral text sentiment
    else:

        if rating >= 4:
            return 'Positive'

        elif rating <= 2:
            return 'Negative'

        else:
            return 'Neutral'


# -------------------- 7. CREATE SENTIMENT BUCKETS -----------
# Group the numerical sentiment scores into four ranges.
# This makes sentiment easier to analyze and visualize.

def sentiment_bucket(score):

    if score >= 0.5:
        return '0.5 to 1.0'

    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'

    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'

    else:
        return '-1.0 to -0.5'


# -------------------- 8. APPLY SENTIMENT ANALYSIS -----------
# Apply the sentiment function to every customer review.
# A new SentimentScore column is created.

customer_reviews_df['SentimentScore'] = (
    customer_reviews_df['ReviewText'].apply(calculate_sentiment)
)


# -------------------- 9. APPLY SENTIMENT CATEGORY -----------
# Apply the categorization function to each row.
# Both SentimentScore and Rating are used.

customer_reviews_df['SentimentCategory'] = (
    customer_reviews_df.apply(
        lambda row: categorize_sentiment(
            row['SentimentScore'],
            row['Rating']
        ),
        axis=1
    )
)


# -------------------- 10. APPLY SENTIMENT BUCKET ------------
# Convert sentiment scores into predefined ranges.

customer_reviews_df['SentimentBucket'] = (
    customer_reviews_df['SentimentScore'].apply(sentiment_bucket)
)


# -------------------- 11. CHECK THE RESULTS -----------------
# Display the first five rows to verify the new columns.
print(customer_reviews_df.head())


# -------------------- 12. EXPORT THE DATA --------------------
# Save the processed DataFrame as a CSV file.
# index=False prevents Pandas from adding an extra index column.

customer_reviews_df.to_csv(
    'fact_customer_reviews_with_sentiment.csv',
    index=False
)
```
