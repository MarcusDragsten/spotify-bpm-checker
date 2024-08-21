from src.entitites.track import TrackAudioFeatures


def calculate_workout_track_score(audio_features: TrackAudioFeatures):
    assert audio_features is not None
    assert audio_features["danceability"]
    assert audio_features["energy"]
    assert audio_features["tempo"]
    assert audio_features["valence"]

    # Normalize tempo to a 0-1 scale (assuming typical workout tempo range of 120 to 160 BPM)
    normalized_tempo = (audio_features["tempo"] - 120) / (160 - 120)
    normalized_tempo = max(0, min(1, normalized_tempo))  # Ensure it's within 0-1

    # Weights for each feature
    weights = {"danceability": 0.15, "energy": 0.6, "tempo": 0.2, "valence": 0.05}

    # Calculate the weighted sum
    score = (
        weights["danceability"] * audio_features["danceability"]
        + weights["energy"] * audio_features["energy"]
        + weights["tempo"] * normalized_tempo
        + weights["valence"] * audio_features["valence"]
    )

    return score
