import pandas  as pd 
import logging 


class RecommendationEngine:
    """
    A class to recommend songs by a specific artist from a DataFrame.
    """

    def __init__(self, df):
        """
        Initialize the RecommendationEngine with a DataFrame containing song data.
        
        :param df: DataFrame with columns 'artist_name', 'genre', 'track_name', and 'info_url'.
        """
        self.df = df
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Set up a logger for the class.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def recommend_songs_by_artist(self, artist_name, n=5):
        """
        Recommend songs by the specified artist.

        :param artist_name: The name of the artist.
        :param n: Number of songs to recommend (default is 5).
        :return: A DataFrame with the top recommended songs.
        """
        try:
            user_filtered_songs = self.df[self.df['artist_name'] == artist_name]
            
             

            sorted_user_filtered_songs = user_filtered_songs.sort_values(by='popularity', ascending=False)

            # Get the top N recommended songs with artist names, genre, track_name, and info_url
            recommended_songs_love = sorted_user_filtered_songs[['artist_name', 'genre', 'track_name', 'info_url']][:n]

            self.logger.info("Recommended Songs:")
            return recommended_songs_love
        except (KeyError, ValueError) as e:
            self.logger.error(f"An error occurred while recommending the data: {str(e)}")
            return pd.DataFrame() 

class RecommendationEngine_forsongs:
    """
    A class to recommend songs by a specific artist from a DataFrame.
    """

    def __init__(self, df):
        """
        Initialize the RecommendationEngine with a DataFrame containing song data.
        
        :param df: DataFrame with columns 'artist_name', 'genre', 'track_name', and 'info_url'.
        """
        self.df = df
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Set up a logger for the class.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
    
    def recommend_songs_on_songs(self, track_name, n=5):
        """
        Recommend songs by the specified artist.

        :param artist_name: The name of the artist.
        :param n: Number of songs to recommend (default is 5).
        :return: A DataFrame with the top recommended songs.
        """
        try:
            user_filtered_songs = self.df[self.df['track_name'] == track_name]
            
             

            sorted_user_filtered_songs = user_filtered_songs.sort_values(by='popularity', ascending=False)

            # Get the top N recommended songs with artist names, genre, track_name, and info_url
            recommended_songs_love = sorted_user_filtered_songs[['artist_name', 'genre', 'track_name', 'info_url','popularity']][:n]

            self.logger.info("Recommended Songs:")
            return recommended_songs_love
        except (KeyError, ValueError) as e:
            self.logger.error(f"An error occurred while recommending the data: {str(e)}")
            return pd.DataFrame()  
        
class SongRecommendation_artist_songs:
    def __init__(self, df):
        """
        Initialize the SongRecommendation class with a DataFrame containing song data.

        :param df: DataFrame with columns 'artist_name', 'genre', 'track_name', 'info_url', and 'popularity'.
        """
        self.df = df

    def recommend_similar_songs_artist(self, artist, song, n=5):
        """
        Recommend songs that are similar to the given artist and song.

        :param artist: The name of the artist.
        :param song: The name of the song.
        :param n: Number of songs to recommend (default is 5).
        :return: A DataFrame with the top recommended songs.
        """
        try:
            # Filter songs by the same artist and a different song (exclude the given song)
            similar_songs = self.df[(self.df['artist_name'] == artist) & (self.df['track_name'] != song)]
            
            # Sort the filtered DataFrame by popularity in descending order
            sorted_similar_songs = similar_songs.sort_values(by='popularity', ascending=False)

            # Get the top N recommended similar songs with artist names, genre, track_name, and info_url
            recommended_songs = sorted_similar_songs[['artist_name', 'genre', 'track_name', 'info_url', 'popularity']][:n]

            return recommended_songs
        except (KeyError, ValueError) as e:
            print(f"An error occurred while recommending similar songs: {str(e)}")
            return pd.DataFrame()
        

def finding_the_most_popular_artist(df,desired_year):
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
        top_n_songs_songs = top_n_songs[['artist_name','track_name','year']]
        return top_n_songs_songs
    except KeyError as e:
        print(f"An error occurred while getting the artist: {str(e)}")
        return None
    except ValueError as e:
        print(f"An error occurred while sorting the songs: {str(e)}")
        return None