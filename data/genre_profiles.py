"""
Shared config for the data generation pipeline: genre list, realistic
per-genre audio-feature profiles, and title generation helpers.
Used by 01_generate_raw_songs.py and kept separate so every pipeline
script references the exact same genre definitions.
"""

N_GENRES = 20

GENRES = [
    "Afrobeats", "Highlife", "Hip-Hop", "R&B", "Pop", "Rock", "Jazz",
    "Classical", "EDM", "House", "Reggae", "Dancehall", "Country",
    "Blues", "Gospel", "Amapiano", "Soul", "Funk", "Indie", "Latin"
]
assert len(GENRES) == N_GENRES

# Realistic per-genre audio feature profiles (mean, std), loosely modeled
# on published genre statistics (e.g. EDM/House run fast and high-energy,
# Classical runs slow/low-energy/high-acoustic, Hip-Hop has high speechiness).
GENRE_PROFILES = {
    #                tempo        energy         valence        dance          loudness(dB)    acoustic       instrumental    speech
    "Afrobeats":  {"tempo": (107, 4),  "energy": (0.75, 0.05), "valence": (0.78, 0.06), "dance": (0.88, 0.04), "loud": (-5.0, 1.0), "acoustic": (0.10, 0.05), "instrumental": (0.05, 0.03), "speech": (0.12, 0.04)},
    "Highlife":   {"tempo": (118, 4),  "energy": (0.60, 0.05), "valence": (0.80, 0.06), "dance": (0.75, 0.05), "loud": (-7.0, 1.2), "acoustic": (0.25, 0.08), "instrumental": (0.10, 0.05), "speech": (0.08, 0.03)},
    "Hip-Hop":    {"tempo": (92, 5),   "energy": (0.65, 0.06), "valence": (0.42, 0.07), "dance": (0.80, 0.05), "loud": (-6.0, 1.0), "acoustic": (0.08, 0.04), "instrumental": (0.02, 0.02), "speech": (0.25, 0.06)},
    "R&B":        {"tempo": (80, 4),   "energy": (0.42, 0.06), "valence": (0.38, 0.07), "dance": (0.62, 0.05), "loud": (-9.0, 1.3), "acoustic": (0.25, 0.08), "instrumental": (0.03, 0.02), "speech": (0.09, 0.03)},
    "Pop":        {"tempo": (120, 5),  "energy": (0.72, 0.05), "valence": (0.68, 0.06), "dance": (0.68, 0.05), "loud": (-5.5, 1.0), "acoustic": (0.12, 0.06), "instrumental": (0.02, 0.02), "speech": (0.06, 0.02)},
    "Rock":       {"tempo": (140, 6),  "energy": (0.90, 0.04), "valence": (0.55, 0.07), "dance": (0.42, 0.06), "loud": (-4.5, 1.0), "acoustic": (0.08, 0.05), "instrumental": (0.15, 0.08), "speech": (0.05, 0.02)},
    "Jazz":       {"tempo": (95, 10),  "energy": (0.32, 0.06), "valence": (0.50, 0.08), "dance": (0.40, 0.06), "loud": (-13.0, 2.0), "acoustic": (0.70, 0.10), "instrumental": (0.55, 0.15), "speech": (0.05, 0.02)},
    "Classical":  {"tempo": (65, 10),  "energy": (0.15, 0.05), "valence": (0.38, 0.08), "dance": (0.20, 0.05), "loud": (-20.0, 3.0), "acoustic": (0.95, 0.04), "instrumental": (0.85, 0.10), "speech": (0.03, 0.01)},
    "EDM":        {"tempo": (130, 3),  "energy": (0.95, 0.03), "valence": (0.72, 0.05), "dance": (0.78, 0.04), "loud": (-3.5, 0.8), "acoustic": (0.03, 0.02), "instrumental": (0.40, 0.15), "speech": (0.06, 0.02)},
    "House":      {"tempo": (123, 2),  "energy": (0.82, 0.04), "valence": (0.65, 0.05), "dance": (0.87, 0.03), "loud": (-4.0, 0.8), "acoustic": (0.04, 0.02), "instrumental": (0.45, 0.15), "speech": (0.06, 0.02)},
    "Reggae":     {"tempo": (75, 4),   "energy": (0.50, 0.05), "valence": (0.72, 0.06), "dance": (0.60, 0.05), "loud": (-8.0, 1.2), "acoustic": (0.20, 0.07), "instrumental": (0.08, 0.04), "speech": (0.08, 0.03)},
    "Dancehall":  {"tempo": (98, 4),   "energy": (0.78, 0.05), "valence": (0.65, 0.06), "dance": (0.85, 0.04), "loud": (-5.5, 1.0), "acoustic": (0.10, 0.05), "instrumental": (0.05, 0.03), "speech": (0.15, 0.04)},
    "Country":    {"tempo": (112, 5),  "energy": (0.52, 0.05), "valence": (0.62, 0.06), "dance": (0.48, 0.05), "loud": (-7.5, 1.2), "acoustic": (0.45, 0.10), "instrumental": (0.04, 0.03), "speech": (0.05, 0.02)},
    "Blues":      {"tempo": (85, 8),   "energy": (0.38, 0.06), "valence": (0.28, 0.07), "dance": (0.35, 0.05), "loud": (-10.0, 1.5), "acoustic": (0.55, 0.12), "instrumental": (0.20, 0.10), "speech": (0.05, 0.02)},
    "Gospel":     {"tempo": (105, 7),  "energy": (0.62, 0.06), "valence": (0.80, 0.05), "dance": (0.50, 0.06), "loud": (-6.5, 1.2), "acoustic": (0.30, 0.09), "instrumental": (0.05, 0.03), "speech": (0.10, 0.04)},
    "Amapiano":   {"tempo": (113, 2),  "energy": (0.66, 0.04), "valence": (0.60, 0.05), "dance": (0.90, 0.03), "loud": (-6.0, 0.9), "acoustic": (0.08, 0.04), "instrumental": (0.35, 0.12), "speech": (0.08, 0.03)},
    "Soul":       {"tempo": (83, 6),   "energy": (0.48, 0.05), "valence": (0.52, 0.06), "dance": (0.58, 0.05), "loud": (-8.5, 1.3), "acoustic": (0.35, 0.09), "instrumental": (0.05, 0.03), "speech": (0.06, 0.02)},
    "Funk":       {"tempo": (110, 4),  "energy": (0.70, 0.05), "valence": (0.72, 0.06), "dance": (0.72, 0.05), "loud": (-6.0, 1.0), "acoustic": (0.12, 0.06), "instrumental": (0.12, 0.06), "speech": (0.07, 0.03)},
    "Indie":      {"tempo": (117, 8),  "energy": (0.52, 0.07), "valence": (0.48, 0.08), "dance": (0.52, 0.06), "loud": (-9.5, 1.5), "acoustic": (0.40, 0.12), "instrumental": (0.10, 0.06), "speech": (0.05, 0.02)},
    "Latin":      {"tempo": (102, 5),  "energy": (0.78, 0.05), "valence": (0.80, 0.06), "dance": (0.80, 0.04), "loud": (-5.0, 0.9), "acoustic": (0.15, 0.06), "instrumental": (0.06, 0.03), "speech": (0.10, 0.03)},
}

# Realistic-ish popularity weighting for genre imbalance in the RAW dataset
# (mainstream genres appear far more often than niche ones, mirroring real
# streaming catalogs). Cleaning does NOT fix this - imbalance is a genuine
# property of the data, not an error, so it survives into the final dataset.
GENRE_POPULARITY_WEIGHT = {
    "Pop": 10, "Hip-Hop": 9, "EDM": 8, "Afrobeats": 8, "R&B": 7,
    "Dancehall": 6, "Amapiano": 6, "Latin": 6, "House": 5, "Rock": 5,
    "Reggae": 4, "Country": 4, "Funk": 4, "Indie": 4, "Gospel": 3,
    "Highlife": 3, "Soul": 3, "Blues": 2, "Jazz": 2, "Classical": 2,
}

TITLE_ADJECTIVES = [
    "Golden", "Silent", "Broken", "Electric", "Midnight", "Endless", "Wild",
    "Fading", "Lost", "Distant", "Velvet", "Crimson", "Hollow", "Radiant",
    "Quiet", "Reckless", "Neon", "Ancient", "Restless", "Gentle", "Burning",
    "Frozen", "Secret", "Sweet", "Forgotten"
]
TITLE_NOUNS = [
    "Horizon", "Heartbeat", "Shadows", "Fire", "Rain", "Dreams", "Skyline",
    "Echoes", "Ocean", "Streets", "Stars", "Memories", "Wind", "Lights",
    "Roads", "Waves", "Ashes", "Bloom", "Storm", "River", "Sky", "Flame",
    "Ground", "Sun", "Moonlight"
]
TITLE_VERBS_ING = [
    "Falling", "Chasing", "Burning", "Dancing", "Drifting", "Waiting",
    "Running", "Glowing", "Breaking", "Calling", "Fading", "Rising"
]


def generate_song_title(rng):
    """Generates a plausible-sounding song title (always 2+ words)."""
    template = rng.integers(0, 4)
    if template == 0:
        return f"{rng.choice(TITLE_ADJECTIVES)} {rng.choice(TITLE_NOUNS)}"
    elif template == 1:
        return f"{rng.choice(TITLE_VERBS_ING)} {rng.choice(TITLE_NOUNS)}"
    elif template == 2:
        n1, n2 = rng.choice(TITLE_NOUNS, size=2, replace=False)
        return f"{n1} in the {n2}"
    else:
        return f"{rng.choice(TITLE_ADJECTIVES)} {rng.choice(TITLE_VERBS_ING)} {rng.choice(TITLE_NOUNS)}"
