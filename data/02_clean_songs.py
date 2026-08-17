"""
02_clean_songs.py

Step 2 of the data pipeline: Cleaning the raw, messy song catalog produced
by 01_generate_raw_songs.py.
"""

import pandas as pd

TEMPO_MIN, TEMPO_MAX = 40, 220
AUDIO_FEATURES = [
    "tempo_bpm", "energy", "valence", "danceability",
    "loudness_db", "acousticness", "instrumentalness", "speechiness",
]


def main():
    raw = pd.read_csv("data/raw/songs_raw.csv")
    n_start = len(raw)
    print(f"Raw dataset: {n_start} rows")

    # 1. Drop missing critical fields
    df = raw.dropna(subset=["title", "artist", "genre"])
    n_after_missing = len(df)
    print(f"After dropping missing title/artist/genre: {n_after_missing} rows "
          f"(-{n_start - n_after_missing})")

    # 2. Drop rows with impossible audio feature values
    df = df[(df["tempo_bpm"] >= TEMPO_MIN) & (df["tempo_bpm"] <= TEMPO_MAX)]
    n_after_invalid = len(df)
    print(f"After dropping invalid tempo values (outside {TEMPO_MIN}-{TEMPO_MAX} BPM): "
          f"{n_after_invalid} rows (-{n_after_missing - n_after_invalid})")

    # 3. Deduplicate - same (title, artist) is the same song scraped
    # multiple times, even if audio feature readings differ slightly
    df = df.drop_duplicates(subset=["title", "artist"], keep="first")
    n_after_dedup = len(df)
    print(f"After deduplicating by (title, artist): {n_after_dedup} rows "
          f"(-{n_after_invalid - n_after_dedup})")

    # 4. Reset to a clean song_id range, keep only the columns downstream code needs
    df = df.reset_index(drop=True)
    df["song_id"] = df.index
    df = df[["song_id", "title", "artist", "genre"] + AUDIO_FEATURES + ["release_year"]]

    df.to_csv("data/songs.csv", index=False)

    print(f"\nCleaned dataset written: data/songs.csv")
    print(f"Final song count: {len(df)}  (from {n_start} raw rows, "
          f"{n_start - len(df)} removed, {100 * len(df) / n_start:.1f}% retained)")
    print(f"\nGenre distribution (cleaned, still imbalanced by design):")
    print(df["genre"].value_counts())


if __name__ == "__main__":
    main()
