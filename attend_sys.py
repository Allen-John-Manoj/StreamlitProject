import sounddevice as sd
import numpy as np
import librosa
import pickle
from scipy.spatial.distance import cosine
import noisereduce as nr

def record_audio(duration=2, sample_rate=22050):
    """ Record audio for a given duration and sample rate, with noise reduction. """
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")

    # Convert the audio array to a 1D numpy array
    audio = audio.flatten()
    
    # Perform noise reduction
    reduced_noise_audio = nr.reduce_noise(y=audio, sr=sample_rate)
    
    return reduced_noise_audio



def extract_features(audio, sample_rate=22050):
    """ Extract enhanced MFCC and delta features from the audio data. """
    mfcc_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
    delta_mfcc_features = librosa.feature.delta(mfcc_features)
    delta2_mfcc_features = librosa.feature.delta(mfcc_features, order=2)
    
    combined_features = np.concatenate((mfcc_features.mean(axis=1), 
                                        delta_mfcc_features.mean(axis=1), 
                                        delta2_mfcc_features.mean(axis=1)))
    return combined_features


def match_audio(live_features, data):
    """ Match live audio features against saved data. """
    best_match = None
    min_distance = float('inf')
    for roll_no, saved_features in data.items():
        # Ensure both vectors are of the same length
        distance = cosine(live_features, saved_features)
        if distance < min_distance:
            min_distance = distance
            best_match = roll_no
    return best_match


def continuous_matching():
    """ Continuously record and match audio until manually stopped. """
    try:
        with open('data.pkl', 'rb') as f:
            saved_data = pickle.load(f)
    except FileNotFoundError:
        print("Data file not found. Please ensure data exists before matching.")
        return
    
    while True:
        audio_data = record_audio(duration=2)
        live_features = extract_features(audio_data)
        match = match_audio(live_features, saved_data)
        
        if match != 'noise':
            print(f"Match found: Roll Number {match}")
            return match
        else:
            print("No match found.")
            return None
        #if input("Press 'q' to quit or any other key to continue: ").lower() == 'q':
         #   break

# Example usage
if __name__ == "__main__":
    while True:
        continuous_matching()
