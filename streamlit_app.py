import streamlit as st
import pandas as pd

from src.data_cleaning import cleaning_the_data, input_cleaning
from src.recommendation import (RecommendationEngine , 
                                RecommendationEngine_forsongs ,
                                SongRecommendation_artist_songs ,
                                finding_the_most_popular_artist)

from src.visualization import (comparing_the_yearly_growth , create_pie_chart ,
                                finding_the_most_popular_artist,
                                plotting_most_popular_artist)

from numerize.numerize import numerize
from dotenv import load_dotenv
import os

load_dotenv()



# Set page configuration
st.set_page_config(page_title="Tune tease", page_icon='🎷', layout='centered')

# Add your CSS styles
st.markdown("""
<style>
    .neon-text {
        position: relative;
        font-family: 'Pacifico', cursive;
        text-transform: uppercase;
        font-size: 5rem; /* Adjust font size as needed */
        color: #FF80AB; /* Neon pink color */
        -webkit-text-stroke-width: 2px;
        -webkit-text-stroke-color: #FF0040; /* Neon pink stroke color */
        text-shadow: 0 0 10px #FF0040,
                     0 0 10px #FF0040,
                     0 0 10px #FF0040;
        z-index: 1;
    }

    .neon-text:after {
        z-index: -1;
        position: absolute;
        color: transparent;
        -webkit-text-stroke-width: 2px;
        -webkit-text-stroke-color: #8000FF; /* Neon purple stroke color */
        top: -5%;
        left: -0.5%;
    }
</style>
""", unsafe_allow_html=True)

# Display the neon text
st.markdown("<h1 class='neon-text'>Tune Tease</h1>", unsafe_allow_html=True)

st.sidebar.title("Tune Tease")
st.sidebar.markdown("Made by [Dame rajee](https://twitter.com/damerajee44)")

with st.sidebar.expander("About"):
    st.markdown("This is a music recommendation app that helps you discover new songs based on your preferences.")
    st.markdown("Simply input your favorite artists, genres, or moods, and let the app suggest the perfect tracks for you.")
    st.markdown("Enjoy your personalized music journey!")
    st.markdown("Please keep in mind the recommendations are limited to 2022") 

st.sidebar.header("Don't forget to check out the vizualization")

raw_file_path = os.environ.get("MY_FILE_PATH")

if raw_file_path:
    file_path = eval(raw_file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        print(f"File data: {data}")
else:
    print("Environment variable MY_FILE_PATH is not set.")

    
@st.cache_data()
def reading_data_st(file_path):
    df = pd.read_csv(file_path)
    clean_df = cleaning_the_data(df)
    uniuqe_year = clean_df['year'].unique()
    return clean_df , uniuqe_year


clean_df,uniuqe_year =reading_data_st(file_path)


def Home(df):
    with st.expander("⏰ My Excel WorkBook"):
        showData = st.multiselect('Filter: ', df.columns,
                                  default=['artist_name', 'track_name', 'popularity', 'year', 'genre', 'track_id', 'info_url'])
        st.dataframe(df[showData], use_container_width=True)
    
        # Compute analytics
    total_popularity = df['popularity'].sum()
    mode_popularity = df['artist_name'].mode().iloc[0]  # Mode can return multiple values, so use iloc[0] to get the first one
    total_year = df['year'].mode().iloc[0]

    total1, total2,total5 = st.columns(3)
        
    with total1:
        st.info('Total Popularity', icon="📌")
        st.metric(label="total popularity", value=f"{total_popularity:,.0f}")

    with total2:
        st.info('Most Frequent Artist', icon="📌")
        st.metric(label="most frequent artist", value=f"{mode_popularity}")
    with total5:
        st.info('Most Frequent Year', icon="📌")
        st.metric(label="most frequent Year", value=total_year, help=f"Total Year: {total_year}")

    st.markdown("---")

# Initialize recommendation engine  
recommendation_engine = RecommendationEngine(clean_df)
recommendation_engine_for_songs = RecommendationEngine_forsongs(clean_df)
recommendation_engine_for_songs_artist = SongRecommendation_artist_songs(clean_df)

# Create two columns within the same form

tab1, tab2= st.tabs(["Recommending songs", "Visualization"])

# Define a list of example artists for the preview
example_artists = ["drake", "sza", "taylor swift","bruno mars"]
default_artists = ", ".join(example_artists)
# Define the default artist for the recommendation input box
default_recommendation_artist = "drake"

with tab1:
    Home(clean_df)
    st.header("Recommending Songs")
    recommendation_placeholder = st.empty()  # Create a placeholder for the recommendation form

    with st.form("recommendation_form"):
        artist = st.text_input("Please enter your desired artist", value=default_recommendation_artist)
        track_name = st.text_input("Please enter your desired song")
        recommendation_type = st.selectbox("Select recommendation type", ["By Artist", "By Song", "By Both"])

        if st.form_submit_button("Recommend"):
            if recommendation_type == "By Artist" and not artist:
                st.warning("Please enter the desired artist.")
            elif recommendation_type == "By Song" and not track_name:
                st.warning("Please enter the desired song.")
            elif recommendation_type == "By Both" and (artist == default_recommendation_artist or not track_name):
                st.warning("Please enter both the artist and the song.")
            else:
                recommendations = None
                if recommendation_type == "By Artist":
                    recommendations = recommendation_engine.recommend_songs_by_artist(input_cleaning(artist))
                elif recommendation_type == "By Song":
                    recommendations = recommendation_engine_for_songs.recommend_songs_on_songs(input_cleaning(track_name))
                elif recommendation_type == "By Both":
                    recommendations = recommendation_engine_for_songs_artist.recommend_similar_songs_artist(input_cleaning(artist), input_cleaning(track_name))

                # Display recommendations as cards
                if recommendations is not None and not recommendations.empty:
                    st.write("**Recommendations:**")
                    for _, row in recommendations.iterrows():
                        col1, col2 = st.columns([1, 2 ])
                        with col1:
                            st.markdown(f"**Artist:** {row['artist_name']}")
                            st.markdown(f"**Genre:** {row['genre']}")
                        with col2:
                            st.markdown(f"**Track:** {row['track_name']}")
                            st.markdown(f"**URL:** {row['info_url']}")
                        
                        st.markdown("---")
                else:
                    st.warning("No recommendations found for the specified criteria.")

        if st.form_submit_button("Clear recommendation"):
            st.markdown(" ")
            
with tab2:
    st.header("Visualization")
    artists_viz = st.text_input("enter your desired artists for visualization (comma-separated)", value=default_artists)
    choice_of_year = clean_df['year'].unique()
    desired_year = st.selectbox("enter the desired year for visualization ",choice_of_year)
    col1, col2 = st.columns(2)

    if st.button("Visualize"):
        artists_list = [artist.strip() for artist in artists_viz.split(",")]
        if not artists_list:
            st.warning('Please enter at least one artist.')
        elif len(artists_list) > 4:
            st.warning('You can select up to 4 artists for visualization.')
        else:
            st.markdown("### Yearly Growth Comparison")
            fig_1 = comparing_the_yearly_growth(clean_df, artists_list)
            st.pyplot(fig_1)
            
            for i, artist in enumerate(artists_list):
                
                fig_3 = create_pie_chart(clean_df, artist)
                
                # Determine where to place the pie chart based on even/odd index
                if i % 2 == 0:
                    with col1:
                        st.pyplot(fig_3)
                else:
                    with col2:
                        st.pyplot(fig_3)
            st.markdown(f"### The top ten most popular artist in the year {desired_year}")
            plottingthe_artist = finding_the_most_popular_artist(clean_df, desired_year)
            yearly_plotting = plottingthe_artist['year'].unique()

            # Call the plotting function to generate the plot and get the figure
            fig_2 = plotting_most_popular_artist(plottingthe_artist, yearly_plotting)

            # Use st.pyplot() to display the Matplotlib plot in Streamlit
            st.pyplot(fig_2)

    if st.button("Clear Plots"):
        st.markdown(" ")
            
