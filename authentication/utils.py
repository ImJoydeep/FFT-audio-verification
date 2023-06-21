import numpy as np
from scipy.fft import fft
from django.http import HttpResponse
from django.http import JsonResponse
import base64




def calculate_fft(audio_data):
    # Perform FFT calculations on audio_data
    # Implement the necessary logic to handle large audio files in chunks
    fft_result = fft(audio_data)
    fft_data = np.abs(fft_result)  # Take the absolute values of the FFT result
    return fft_data.tolist()

def matching_algorithm(fft_features1, fft_features2):
    # Implement your matching algorithm here
    # This is a simple example that calculates the cosine similarity between the two feature arrays

    # Calculate the cosine similarity
    dot_product = np.dot(fft_features1, fft_features2)
    norm_product = np.linalg.norm(fft_features1) * np.linalg.norm(fft_features2)
    similarity = dot_product / norm_product

    if similarity >= 0.5:
        return similarity
    else:
        return 0.0



def handle_uploaded_file(file):
    # Read the file's contents
    file_data = file.read()

    # Determine the file encoding (if known)
    file_encoding = 'utf-8'  # Update this with the correct encoding if known

    # Convert the file data to a NumPy array
    # Here, we assume the file contains numeric data in text format with one value per line
    try:
        file_data_str = file_data.decode(file_encoding)
    except UnicodeDecodeError:
        return JsonResponse({'error': 'Unable to decode file data.'})

    file_data_list = file_data_str.split('\n')
    file_data_float = [float(value) for value in file_data_list if value]
    file_data_np = np.array(file_data_float)

    # Apply the FFT
    fft_result = np.fft.fft(file_data_np)
    print(type(fft_result))

    # Process the FFT result
    # For example, let's calculate the amplitude spectrum
    amplitude_spectrum = np.abs(fft_result)

    # Convert the amplitude spectrum to a list for JSON serialization
    amplitude_spectrum_list = amplitude_spectrum.tolist()

    # Return a JSON response with the amplitude spectrum
    return int(file_data_np)


