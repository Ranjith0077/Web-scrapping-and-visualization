import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def visual():
    # Connect to the SQLite database
    conn = sqlite3.connect('DB\movies.db')
    cursor = conn.cursor()
    # Query the top 10 movies by rating and voting counts
    df = pd.read_sql_query("SELECT * FROM movies ORDER BY Rating DESC, Votes DESC LIMIT 10", conn)


    # Streamlit app
    st.title("IMDB 2024 Data Scraping and Visualizations")

    # Display the DataFrame in Streamlit
    st.write("Here are the top 10 movies:")
    st.dataframe(df)

    # Visualization: Bar plot for Ratings
    st.subheader("Top 10 Movies by Rating")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Rating", y="Title", data=df, palette="viridis")
    plt.xlabel("Rating")
    plt.ylabel("Movie Title")
    plt.title("Top 10 Movies by Rating")
    st.pyplot(plt)

    # Visualization: Bar plot for Votes
    st.subheader("Top 10 Movies by Votes")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Votes", y="Title", data=df, palette="magma")
    plt.xlabel("Votes")
    plt.ylabel("Movie Title")
    plt.title("Top 10 Movies by Votes")
    st.pyplot(plt)

    #Genre Distribution: Plot the count of movies for each genre in a bar chart.

    #Query all movies to get genre data
    df = pd.read_sql_query("SELECT * FROM movies", conn)

    # Split the genres into separate rows for counting
    df = df.explode('Genre')  # Split genres if they are comma-separated in a single row

    # Count the number of movies for each genre
    genre_counts = df['Genre'].value_counts()
    print(genre_counts)

    st.subheader("Genre Distribution")
    genre_counts = df['Genre'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_counts.index, y=genre_counts.values, palette="coolwarm")
    plt.xlabel("Genre")
    plt.ylabel("Count")
    plt.title("Genre Distribution of Top 10 Movies")
    st.pyplot(plt)  

    #Average Duration by Genre: Show the average movie duration per genre in a horizontal bar chart.
    #Sql query to get average duration by genre
    df = pd.read_sql_query("SELECT Genre, AVG(Duration) as Average_Duration FROM movies GROUP BY Genre", conn)
    df['Average_Duration'] = df['Average_Duration'].astype(float)  # Ensure it's float for plotting
    df = df.sort_values(by='Average_Duration', ascending=False)  # Sort by average duration
    print(df)

    st.subheader("Average Duration by Genre")
    average_duration = df.groupby('Genre')['Average_Duration'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=average_duration.values, y=average_duration.index, palette="crest")
    plt.xlabel("Average Duration (minutes)")
    plt.ylabel("Genre")
    plt.title("Average Duration by Genre")
    st.pyplot(plt)

    #Voting Trends by Genre: Visualize average voting counts across different genres.
    #Sql query to get voting trends by genre
    df = pd.read_sql_query("SELECT Genre, AVG(Votes) as Average_Votes FROM movies GROUP BY Genre", conn)
    df['Average_Votes'] = df['Average_Votes'].astype(float)  # Ensure it's float for plotting
    df = df.sort_values(by='Average_Votes', ascending=False)  # Sort by average votes
    print(df)
    st.write("Genres in the dataset:")
    st.write(df['Genre'].unique())
    st.subheader("Voting Trends by Genre")
    average_votes = df.groupby('Genre')['Average_Votes'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=average_votes.values, y=average_votes.index, palette="rocket")
    plt.xlabel("Average Votes")
    plt.ylabel("Genre")
    plt.title("Voting Trends by Genre")
    st.pyplot(plt)

    #Rating Distribution: Display a histogram or boxplot of movie ratings.
    #Sql query to get rating distribution
    df = pd.read_sql_query("SELECT Rating FROM movies", conn)
    df['Rating'] = df['Rating'].astype(float)  # Ensure it's float for plotting
    print(df['Rating'])
    
    st.subheader("Rating Distribution")
    plt.figure(figsize=(10, 6)) 

    sns.histplot(df['Rating'], bins=10, kde=True, color='blue')
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title("Rating Distribution of Top 10 Movies")
    st.pyplot(plt)

    #Genre-Based Rating Leaders: Highlight the top-rated movie for each genre in a table.
    #Sql query to get genre-based rating leaders
    df = pd.read_sql_query("SELECT Genre, Title, Rating FROM movies ORDER BY Rating DESC", conn)
    df['Rating'] = df['Rating'].astype(float)  # Ensure it's float for plotting
    df = df.groupby('Genre').first().reset_index()  # Get the first movie for each genre
    print(df)
    st.subheader("Genre-Based Rating Leaders")
    st.write("Top-rated movie for each genre:")
    st.dataframe(df[['Genre', 'Title', 'Rating']])

    #Most Popular Genres by Voting: Identify genres with the highest total voting counts in a pie chart.
    #Sql query to get most popular genres by voting
    df = pd.read_sql_query("SELECT Genre, SUM(Votes) as Total_Votes FROM movies GROUP BY Genre", conn)
    df['Total_Votes'] = df['Total_Votes'].astype(float)  # Ensure it's float for plotting
    df = df.sort_values(by='Total_Votes', ascending=False)  # Sort by total votes
    print(df)
    st.subheader("Most Popular Genres by Voting")
    plt.figure(figsize=(10, 6))
    plt.pie(df['Total_Votes'], labels=df['Genre'], autopct='%1.1f%%', startangle=140)
    plt.title("Most Popular Genres by Voting")
    st.pyplot(plt)

    #Duration Extremes: Use a table or card display to show the shortest and longest movies.
    #Sql query to get duration extremes
    df = pd.read_sql_query("SELECT Title, Duration FROM movies ORDER BY Duration ASC", conn)    
    df['Duration'] = df['Duration'].astype(float)  # Ensure it's float for plotting
    df = df.head(1)  # Get the shortest movie
    shortest_movie = df.iloc[0]
    print(shortest_movie)
    st.subheader("Shortest Movie")
    st.write(f"Title: {shortest_movie['Title']}, Duration: {shortest_movie['Duration']} minutes")
    
    df = pd.read_sql_query("SELECT Title, Duration FROM movies ORDER BY Duration DESC", conn)
    df['Duration'] = df['Duration'].astype(float)  # Ensure it's float for plotting
    df = df.head(1)  # Get the longest movie
    longest_movie = df.iloc[0]
    print(longest_movie)
    st.subheader("Longest Movie")
    st.write(f"Title: {longest_movie['Title']}, Duration: {longest_movie['Duration']} minutes")


    #Ratings by Genre: Use a heatmap to compare average ratings across genres.
    #Sql query to get ratings by genre
    df = pd.read_sql_query("SELECT Genre, Rating FROM movies", conn)
    df['Rating'] = df['Rating'].astype(float)  # Ensure it's float for plotting
    df = df.explode('Genre')  # Split genres if they are comma-separated in a single row
    
    df = df.groupby(['Genre', 'Rating']).size().unstack(fill_value=0)  # Create a pivot table
    print(df)
    st.subheader("Ratings by Genre")
    plt.figure(figsize=(10, 6))
    sns.heatmap(df, annot=True, cmap="YlGnBu", fmt="d")
    plt.title("Ratings by Genre")
    st.pyplot(plt)


    #Correlation Analysis: Analyze the relationship between ratings and voting counts using a scatter plot.
    #Sql query to get correlation analysis
    df = pd.read_sql_query("SELECT Rating, Votes FROM movies", conn)
    df['Rating'] = df['Rating'].astype(float)  # Ensure it's float for plotting
    df['Votes'] = df['Votes'].astype(float)  # Ensure it's float for plotting
    print(df)
    st.subheader("Correlation Analysis")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="Votes", y="Rating", data=df, color='purple')
    plt.xlabel("Votes")
    plt.ylabel("Rating")
    plt.title("Correlation between Votes and Rating")
    st.pyplot(plt)

    # Close the database connection
    conn.close()


    