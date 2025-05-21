from wave import open as wave_open
import struct
import os

EXTRACTED_FOLDER = 'static/extracted/'

def decode(input_file_path):
    with wave_open(input_file_path, 'rb') as wave_in:
        n_frames = wave_in.getnframes()
        frames = wave_in.readframes(n_frames)

    frame_bytes = bytearray(frames)
    # extracted_bits = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    extracted_bits = [frame_bytes[i * 2] & 1 for i in range(len(frame_bytes) // 2)]


    byte_chunks = [''.join(map(str, extracted_bits[i:i+8])) for i in range(0, len(extracted_bits), 8)]
    extracted_bytes = bytearray(int(byte, 2) for byte in byte_chunks)

    if b'###' in extracted_bytes:
        extracted_data = extracted_bytes.split(b'###')[0]
        try:
            extracted_text = extracted_data.decode('utf-8')
            return extracted_text, None
        except UnicodeDecodeError:
            pass  

    extracted_image_path = os.path.join(EXTRACTED_FOLDER, "extracted_image.png")
    with open(extracted_image_path, 'wb') as img_file:
        img_file.write(extracted_bytes.split(b'###')[0])

    return None, extracted_image_path
