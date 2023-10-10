import seaborn as sns 
import matplotlib.pyplot as plt 


def comparing_the_yearly_growth(df, target_artists):
    
    plt.figure(figsize=(8, 5))

    if isinstance(target_artists, str):
        # If target_artists is a single string, convert it to a list for consistency
        target_artists = [target_artists]

    for artist in target_artists:
        # Filter the DataFrame to select data for the specific artist
        artist_data = df[df['artist_name'] == artist]

        # Determine the columns dynamically
        columns = {
            'artist_name': None,
            'year': None,
            'popularity': None
        }

        for column in df.columns:
            for key in columns:
                if key in column.lower():
                    columns[key] = column

        if all(columns.values()):
            # Group the data by 'year' and calculate the mean popularity for each year
            popularity_growth = artist_data.groupby(columns['year'])[columns['popularity']].mean()

            # Plot the popularity growth for the artist
            plt.plot(popularity_growth.index, popularity_growth.values, marker='o', linestyle='-', label=artist)

    plt.title(f'Popularity Growth for {target_artists} Over Time')
    plt.xlabel('Year')
    plt.ylabel('Mean Popularity')
    plt.legend()
    plt.grid(True)

    return plt.gcf()

def create_pie_chart(df, target_artist):
    # Convert the target_artist name to lowercase for case-insensitive matching
    target_artist = target_artist.lower()

    # Filter the DataFrame to select data for the specific artist
    artist_data = df[df['artist_name'].str.lower() == target_artist]

    if artist_data.empty:
        return None  # Return None if the artist is not found in the DataFrame

    # Determine the columns dynamically
    columns = {
        'artist_name': None,
        'genre': None,
        'popularity': None
    }

    for column in df.columns:
        for key in columns:
            if key in column.lower():
                columns[key] = column

    if all(columns.values()):
        # Group the data by 'genre' and calculate the sum of popularity for each genre
        genre_popularity = artist_data.groupby(columns['genre'])[columns['popularity']].sum()

        # Create a pie chart to visualize genre popularity for the artist
        plt.figure(figsize=(8, 7))
        
        # Determine the number of genres for explode parameter
        num_genres = len(genre_popularity)
        explode = tuple(0.1 for _ in range(num_genres))  # Explode slices for emphasis
        
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
        
        plt.pie(
            genre_popularity,
            labels=genre_popularity.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            explode=explode,
            shadow=True
        )
        plt.title(f'Genre Popularity Distribution for {target_artist}', fontsize=16)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        return plt  # Return the Matplotlib figure for the pie chart

    return None


def finding_the_most_popular_artist(df, desired_year:int):
    try:
        
        if 'year' not in df.columns or 'popularity' not in df.columns:
            raise KeyError("The 'year' or 'popularity' columns do not exist in the DataFrame.")

        songs_in_desired_year = df[df['year'] == desired_year]

        # Check if there are any songs for the desired year
        if songs_in_desired_year.empty:
            print(f"No songs found for the year {desired_year}.")
            return None

        sorted_songs = songs_in_desired_year.sort_values(by='popularity', ascending=False)
        top_n_songs = sorted_songs.head(10)
        top_n_songs_songs = top_n_songs[['artist_name','track_name','year','popularity']]
        return top_n_songs_songs
    except KeyError as e:
        print(f"An error occurred while getting the artist: {str(e)}")
        return None
    except ValueError as e:
        print(f"An error occurred while sorting the songs: {str(e)}")
        return None
    
def plotting_most_popular_artist(df,yearly_plotting:int):
    colors = ['royalblue', 'forestgreen', 'firebrick', 'gold', 'mediumorchid', 'dodgerblue', 'limegreen', 'tomato', 'indigo', 'orange']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['artist_name'], df['popularity'], color=colors)
    ax.set_xlabel('Popularity', fontsize=12)
    ax.set_ylabel('Artist Name', fontsize=12)
    ax.set_title(f'Top Ten Artists by Popularity in the year: {yearly_plotting}', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)

    # Remove background color
    ax.set_facecolor('none')

    # Add data labels
    for i, v in enumerate(df['popularity']):
        ax.text(v + 1, i, str(v), color='black', va='center', fontsize=10, fontweight='bold')

    ax.tick_params(axis='both', which='major', labelsize=10)

    plt.tight_layout()

    return fig