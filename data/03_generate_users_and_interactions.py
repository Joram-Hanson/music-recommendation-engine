"""
03_generate_users_and_interactions.py

Step 3 of the data pipeline: generating users, hidden ground-truth genre
preferences, and interaction events - built on top of the CLEANED song
catalog from 02_clean_songs.py (data/songs.csv), not the raw one.
"""

import numpy as np
import pandas as pd
from faker import Faker
import random

from genre_profiles import GENRES, N_GENRES

N_USERS = 400
SEED = 42

rng = np.random.default_rng(SEED)
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)


def generate_users_and_ground_truth():
    users = []
    ground_truth = []
    for u in range(N_USERS):
        age_bracket = random.choice(["13-17", "18-24", "25-34", "35-44", "45+"])
        listening_time = random.choice(["morning", "afternoon", "evening", "night"])
        users.append({
            "user_id": u,
            "username": fake.user_name(),
            "age_bracket": age_bracket,
            "preferred_listening_time": listening_time,
        })

        # Hidden preference vector: each user strongly likes 2-3 genres,
        # mildly likes a few more, and is indifferent/dislikes the rest.
        pref = rng.dirichlet(np.full(N_GENRES, 0.15))
        row = {"user_id": u}
        for g_idx, g in enumerate(GENRES):
            row[g] = round(pref[g_idx], 5)
        ground_truth.append(row)

    return pd.DataFrame(users), pd.DataFrame(ground_truth)


def generate_interactions(users_df, songs_df, gt_df):
    interactions = []
    gt_lookup = gt_df.set_index("user_id")
    n_songs = len(songs_df)

    for u in users_df["user_id"]:
        pref_vector = gt_lookup.loc[u]
        n_interactions = rng.integers(40, 81)

        song_weights = songs_df["genre"].map(pref_vector).values
        song_weights = 0.85 * song_weights + 0.15 * (1 / n_songs)
        song_weights = song_weights / song_weights.sum()

        sampled_song_idxs = rng.choice(
            songs_df.index, size=n_interactions, replace=True, p=song_weights
        )

        for idx in sampled_song_idxs:
            song = songs_df.loc[idx]
            match_strength = pref_vector[song["genre"]]

            play_prob = np.clip(0.3 + match_strength * 3, 0.05, 0.97)
            played_fully = rng.random() < play_prob
            liked = played_fully and (rng.random() < 0.6)
            skipped = not played_fully

            interactions.append({
                "user_id": u,
                "song_id": song["song_id"],
                "played_fully": played_fully,
                "skipped": skipped,
                "liked": liked,
                "rating": rng.integers(1, 6) if rng.random() < 0.3 else None,
            })

    return pd.DataFrame(interactions)


def main():
    songs_df = pd.read_csv("data/songs.csv")  # the CLEANED catalog from step 2
    print(f"Loaded cleaned song catalog: {len(songs_df)} songs")

    users_df, gt_df = generate_users_and_ground_truth()
    interactions_df = generate_interactions(users_df, songs_df, gt_df)

    users_df.to_csv("data/users.csv", index=False)
    interactions_df.to_csv("data/interactions.csv", index=False)
    gt_df.to_csv("data/ground_truth.csv", index=False)

    print(f"Users:        {len(users_df)} rows -> data/users.csv")
    print(f"Interactions: {len(interactions_df)} rows -> data/interactions.csv")
    print(f"Ground truth: {len(gt_df)} rows -> data/ground_truth.csv (EVAL ONLY)")


if __name__ == "__main__":
    main()
