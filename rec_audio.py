import sounddevice as sd
import numpy as np
import librosa
import pickle
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


def save_data(roll_no, features, filename='data.pkl'):
    """ Save the roll number and features to a file. """
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = {}
    
    data[roll_no] = features
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def record_students(number_of_students):
    """ Record audio data for a specified number of students. """
    for _ in range(number_of_students):
        roll_no = input("Enter the student's roll number or type 'exit' to finish: ")
        if roll_no.lower() == 'exit':
            break
        name = input("Enter name of ", roll_no)
        audio_data = record_audio(duration=5)
        features = extract_features(audio_data)
        save_data(roll_no, name, features)
        print(f"Data saved for {roll_no}, {name}")

# Example usage
if __name__ == "__main__":
    number_of_students = 72  # Set this to any number of students you expect
    record_students(number_of_students)
