import pytest 
import pandas  as pd 


from data.data_ingestion import read_the_data
from src.data_cleaning import cleaning_the_data
from src.recommendation import RecommendationEngine , SongRecommendation_artist_songs ,RecommendationEngine_forsongs


file_path = r"F:\mlops0\data\filtered_data.csv"

@pytest.fixture
def recommendation_engine():
    # Initialize and return your recommendation engine
    
    data = read_the_data(file_path)
    clean_data = cleaning_the_data(data)
    uniuqe_year = clean_data['year'].unique()
    print("uniuqe_year :",uniuqe_year)
    recommend = RecommendationEngine(clean_data)
    recommend_songs = RecommendationEngine_forsongs(clean_data)
    recommend_songs_and_artist = SongRecommendation_artist_songs(clean_data)
    return recommend, recommend_songs , recommend_songs_and_artist,uniuqe_year
   
def test_recommend_songs_by_artist_empty(recommendation_engine):
    # Test when the specified artist does not exist in the dataset
    artist_name = "Nonexistent Artist"
    recommended_songs = recommendation_engine[0].recommend_songs_by_artist(artist_name)
    assert recommended_songs.empty

def test_recommend_songs_by_artists_valid(recommendation_engine):
    # Test when a valid artist name is specified
    artist_name = "Drake"
    recommend = recommendation_engine[0].recommend_songs_by_artist(artist_name)
    assert recommend is not None

def test_recommend_songs_by_songs_empty(recommendation_engine):
    # Test when the specified song does not exist in the dataset
    song_name = "Nonexistent Song"
    recommended_songs = recommendation_engine[1].recommend_songs_on_songs(song_name)
    assert recommended_songs.empty

def test_recommend_songs_by_songs_valid(recommendation_engine):
    # Test when a valid song name is specified
    song_name = "Rich Flex"
    recommend = recommendation_engine[1].recommend_songs_on_songs(song_name)
    assert recommend is not None

def test_recommend_songs_by_songs_artist_empty(recommendation_engine):
    # Test when the specified song does not exist in the dataset
    song_name = "Nonexistent Song"
    artist_name = "Nonexistent Artist"
    recommended_songs = recommendation_engine[2].recommend_similar_songs_artist(song_name ,artist_name)
    assert recommended_songs.empty 

def test_recommend_songs_by_songs__artist_valid(recommendation_engine):
    # Test when a valid song name is specified
    song_name = "Rich Flex"
    artist_name = "Drake"
    recommend = recommendation_engine[2].recommend_similar_songs_artist(song_name,artist_name)
    assert recommend is not None