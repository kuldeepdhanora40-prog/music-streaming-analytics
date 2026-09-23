# Music Streaming Analytics & Insights

## Project Overview
This project converts a Spotify-style music tracks dataset into a business-intelligence dashboard with KPIs, genre and artist comparisons, audio-feature analysis, filters and dataset-driven insights.

## Dataset Used
**File:** `dataset.csv`  
**Rows:** 114,000  
**Columns:** 20  
**Unique artists:** 31,437  
**Unique genres:** 114  
**Average popularity:** 33.24

The uploaded dataset contains fields including `track_id`, `artists`, `album_name`, `track_name`, `popularity`, `duration_ms`, `explicit`, `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `time_signature`, and `track_genre`.

**Original dataset source:** https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

## Key Questions
1. How popular are tracks overall?
2. Which genres have higher average popularity?
3. Which artists are strongly represented?
4. How do audio features such as danceability and energy relate to popularity?
5. What descriptive insights can be turned into content or catalogue decisions?

## Main Features
- KPI cards for tracks, artists, genres, average popularity and duration
- Popularity distribution
- Genre popularity comparison
- Danceability vs energy visualization
- Artist analysis
- Genre volume analysis
- Interactive genre/popularity filters
- Automatic dataset-driven insights

## Technologies
Python, Pandas, NumPy, Matplotlib, Streamlit.

## How to Run
```bash
pip install -r requirements.txt
streamlit run music_analytics.py
```

## Project Files
```text
music-analytics/
├── music_analytics.py
├── dataset.csv
├── requirements.txt
├── README.md
└── Project_Report.docx
```

## Important Submission Note
Keep the dataset attribution/source in the final submission. Do not claim causal relationships from simple correlations. The project is an analytics/BI project; a prediction model is not required.

## Sample Findings From This Dataset
- Average popularity: 33.24
- Median popularity: 35.00
- Highest-average-popularity genre: pop-film (59.28)
- Most represented artist: The Beatles (279 tracks)

These are descriptive findings from the supplied dataset and may change if the dataset is replaced.
