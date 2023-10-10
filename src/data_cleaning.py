import pandas as pd 
import logging 




def create_url(track_id):
    base_url = 'https://open.spotify.com/track/'
    return base_url +  track_id  



def cleaning_the_data(df):
    try:
        # First, take only a subset of the data
        df_new = df[['artist_name','track_name','popularity','year' ,'genre','track_id']]

        filtered_df = df_new[df_new['popularity'] > 20]
        
        filtered_df.reset_index(drop=True, inplace=True)
        filtered_df['clean_track_name'] = filtered_df['track_name'].str.lower()
        filtered_df['clean_track_name'] = filtered_df['clean_track_name'].str.replace(r'\s+', '', regex=True)
        filtered_df['clean_track_name'] = filtered_df['clean_track_name'].fillna('')
        # Apply the function to the 'clean_track_name' and 'track_id' columns to create 'info_url'
        # Apply the function to the 'clean_track_name' and 'track_id' columns to create 'info_url'
        filtered_df['info_url'] = filtered_df.apply(lambda row: create_url(row['track_id']), axis=1)

        filtered_df.drop(columns=['clean_track_name'],inplace=True)
        filtered_df['track_name'] = filtered_df['track_name'].str.lower()
        filtered_df['artist_name'] = filtered_df['artist_name'].str.lower()
        filtered_df['track_name'] = filtered_df['track_name'].str.strip()
        filtered_df['artist_name'] = filtered_df['artist_name'].str.strip()

        return filtered_df
    
    except Exception as e:
        logging.error(f"An error occurred while cleaning the data: {str(e)}")
        return None
    
def input_cleaning(user_input: str):
    if user_input is not None:
       
        lower_input = user_input.lower()
        cleaned_input = lower_input.strip()

        return cleaned_input
    else:
        return None