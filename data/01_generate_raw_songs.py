"""
01_generate_raw_songs.py

We  generated a RAW, deliberately messy song
catalog (~40,000 rows) simulating what a scraped/merged real-world music
dataset often looks like before cleaning:
"""

import numpy as np
import pandas as pd
from faker import Faker

from genre_profiles import GENRES, GENRE_PROFILES, GENRE_POPULARITY_WEIGHT, generate_song_title

SEED = 42
N_UNIQUE_TARGET = 22000  # unique songs before duplication/junk injection

rng = np.random.default_rng(SEED)
fake = Faker()
Faker.seed(SEED)


def _clip01(x):
    return float(np.clip(x, 0.0, 1.0))


def genre_weights():
    weights = np.array([GENRE_POPULARITY_WEIGHT[g] for g in GENRES], dtype=float)
    return weights / weights.sum()


def sample_features(genre, rng_local):
    profile = GENRE_PROFILES[genre]
    return {
        "tempo_bpm": round(max(40, rng_local.normal(*profile["tempo"])), 1),
        "energy": round(_clip01(rng_local.normal(*profile["energy"])), 3),
        "valence": round(_clip01(rng_local.normal(*profile["valence"])), 3),
        "danceability": round(_clip01(rng_local.normal(*profile["dance"])), 3),
        "loudness_db": round(rng_local.normal(*profile["loud"]), 2),
        "acousticness": round(_clip01(rng_local.normal(*profile["acoustic"])), 3),
        "instrumentalness": round(_clip01(rng_local.normal(*profile["instrumental"])), 3),
        "speechiness": round(_clip01(rng_local.normal(*profile["speech"])), 3),
    }


def generate_unique_songs(n):
    weights = genre_weights()
    rows = []
    for i in range(n):
        genre = rng.choice(GENRES, p=weights)
        row = {
            "raw_id": i,
            "title": generate_song_title(rng),
            "artist": fake.name(),
            "genre": genre,
            "release_year": int(rng.integers(1990, 2026)),
        }
        row.update(sample_features(genre, rng))
        rows.append(row)
    return pd.DataFrame(rows)


def inject_duplicates(df, dup_fraction=0.52, max_extra_copies=2):
    """
    For a random subset of songs, add 1-2 extra near-duplicate rows with
    the same title/artist/genre but slightly perturbed audio features -
    simulating the same track being scraped from multiple sources.
    """
    n_dup_candidates = int(len(df) * dup_fraction)
    dup_indices = rng.choice(df.index, size=n_dup_candidates, replace=False)

    extra_rows = []
    next_id = df["raw_id"].max() + 1
    for idx in dup_indices:
        base = df.loc[idx]
        n_copies = rng.integers(1, max_extra_copies + 1)
        for _ in range(n_copies):
            dup_row = base.copy()
            dup_row["raw_id"] = next_id
            next_id += 1
            # small measurement-noise-style perturbation on audio features
            for feat in ["tempo_bpm", "energy", "valence", "danceability",
                         "loudness_db", "acousticness", "instrumentalness", "speechiness"]:
                noise = rng.normal(0, 0.01) if feat != "tempo_bpm" else rng.normal(0, 0.5)
                dup_row[feat] = dup_row[feat] + noise
            extra_rows.append(dup_row)

    return pd.concat([df, pd.DataFrame(extra_rows)], ignore_index=True)


def inject_junk_rows(df, junk_fraction=0.015):
    """
    Corrupt a small fraction of rows to simulate real-world scraping
    issues: missing artist/title, or impossible audio feature values.
    """
    n_junk = int(len(df) * junk_fraction)
    junk_indices = rng.choice(df.index, size=n_junk, replace=False)

    for idx in junk_indices:
        corruption_type = rng.integers(0, 3)
        if corruption_type == 0:
            df.loc[idx, "artist"] = None
        elif corruption_type == 1:
            df.loc[idx, "title"] = None
        else:
            # impossible tempo (sensor/scraping error)
            df.loc[idx, "tempo_bpm"] = rng.choice([-15.0, 410.0, 0.0])

    return df


def main():
    print(f"Generating {N_UNIQUE_TARGET} unique songs (weighted by genre popularity)...")
    unique_songs = generate_unique_songs(N_UNIQUE_TARGET)

    print("Injecting near-duplicate rows (simulating multi-source scraping)...")
    with_dupes = inject_duplicates(unique_songs)

    print("Injecting a small fraction of corrupted/invalid rows...")
    raw = inject_junk_rows(with_dupes)

    raw = raw.sample(frac=1.0, random_state=SEED).reset_index(drop=True)  # shuffle

    raw.to_csv("data/raw/songs_raw.csv", index=False)

    print(f"\nRaw dataset written: data/raw/songs_raw.csv")
    print(f"Total raw rows: {len(raw)}")
    print(f"  Unique songs originally generated: {N_UNIQUE_TARGET}")
    print(f"  Duplicate/near-duplicate rows added: {len(raw) - N_UNIQUE_TARGET - int(N_UNIQUE_TARGET * 0.015)}")
    print(f"\nGenre distribution (raw, imbalanced by design):")
    print(raw["genre"].value_counts())


if __name__ == "__main__":
    main()
