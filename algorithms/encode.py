from wave import open as wave_open
import struct
import os

def encode(input_file_path, output_file_path, secret_message=None, image_path=None):
    with wave_open(input_file_path, 'rb') as wave_in:
        params = wave_in.getparams()
        n_frames = wave_in.getnframes()
        frames = wave_in.readframes(n_frames)

    frame_bytes = bytearray(frames)

    if image_path:
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        image_data += b'###'  # Delimiter for image
        bits = list(map(int, ''.join(f'{byte:08b}' for byte in image_data)))
    else:
        secret_message += '###'  # Delimiter for text
        bits = list(map(int, ''.join(f'{ord(c):08b}' for c in secret_message)))

    if len(bits) > len(frame_bytes):
        raise ValueError("Secret data is too large to encode in this audio file.")

    # for i, bit in enumerate(bits):
    #     frame_bytes[i] = (frame_bytes[i] & 254) | bit
    for i, bit in enumerate(bits):
     frame_bytes[i * 2] = (frame_bytes[i * 2] & 254) | bit  # Use every 2nd byte


    with wave_open(output_file_path, 'wb') as wave_out:
        wave_out.setparams(params)
        wave_out.writeframes(frame_bytes)
