from src.entitites.track import TrackAudioFeatures


def calculate_sleepy_track_score(audio_features: TrackAudioFeatures):

    assert audio_features is not None
    assert audio_features["acousticness"]
    assert audio_features["liveness"]
    assert audio_features["energy"]
    assert audio_features["loudness"]
    assert audio_features["tempo"]

    # Weights for each feature
    weights = {
        "acousticness": 0.15,
        "liveness": 0.05,
        "energy": 0.4,
        "tempo": 0.2,
        "loudness": 0.2
    }

    # Normalize tempo and loudness
    normalized_tempo = (audio_features["tempo"] - 60) / (120 - 60)
    normalized_loudness = (audio_features["loudness"] + 60) / 60

    # Calculate the weighted sum
    score = (
        weights["acousticness"] * audio_features["acousticness"]
        + weights["liveness"] * audio_features["liveness"]
        + weights["energy"] * (1 - audio_features["energy"])  # Invert energy effect
        + weights["tempo"] * (1 - normalized_tempo)  # Invert tempo effect
        + weights["loudness"] * (1 - normalized_loudness)  # Invert loudness effect
    )

    return score
