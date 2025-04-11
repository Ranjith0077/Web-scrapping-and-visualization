import streamlit as st
import pandas as pd
import sqlite3

def filtered():
    # Connect to the SQLite database
    conn = sqlite3.connect('movies.db')

    # Load data from the database
    query = "SELECT * FROM movies"
    movies_df = pd.read_sql(query, conn)

    # Streamlit app
    st.title("Movies 2024 Database")

    # Filter by genre
    genres = movies_df['Genre'].unique().tolist()
    selected_genres = st.multiselect("Select Genres", genres, default=genres)

    # Filter by rating
    min_rating = st.slider("Minimum Rating", 0.0, 10.0, 5.0)

    # Filter by duration
    duration_filter = st.selectbox("Select Duration", ["< 2 hrs", "2–3 hrs", "> 3 hrs"])

    # Filter by voting counts
    min_votes = st.number_input("Minimum Votes", min_value=0, value=10000)

    # Apply filters
    filtered_df = movies_df[movies_df['Genre'].isin(selected_genres)]
    filtered_df = filtered_df[filtered_df['Rating'].astype(float) >= min_rating]
    print(filtered_df['Duration'])
    if duration_filter == "< 2 hrs":
        filtered_df = filtered_df[filtered_df['Duration'] < 120]
    elif duration_filter == "2–3 hrs":
        filtered_df = filtered_df[(filtered_df['Duration'] >= 120) & 
                                (filtered_df['Duration'] <= 180)]
    elif duration_filter == "> 3 hrs":
        filtered_df = filtered_df[filtered_df['Duration'] > 180]

    filtered_df = filtered_df[filtered_df['Votes'] >= min_votes]

    # Display the filtered data
    st.write(f"Movies with rating >= {min_rating}, duration {duration_filter}, votes >= {min_votes}, and genres {', '.join(selected_genres)}")
    st.dataframe(filtered_df)

    conn.close()

def main():
    st.title("Movies 2024 Database")
    button=st.button("filter movies")
    if button:
        filtered()
    
    
if __name__ == "__main__":
    main()