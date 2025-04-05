import threading

import sounddevice as sd
import soundfile as sf

CHUNK_SIZE = 1024


def play_on_device(
    device_id: int,
    sound: sf.SoundFile,
):
    input_device_stream = sd.OutputStream(
        blocksize=CHUNK_SIZE,
        samplerate=sound.samplerate,
        channels=sound.channels,
        dtype="float32",
    )
    output_device_stream = sd.OutputStream(
        device=device_id,
        blocksize=CHUNK_SIZE,
        samplerate=sound.samplerate,
        channels=sound.channels,
        dtype="float32",
    )

    input_device_stream.start()
    output_device_stream.start()

    stremed = 0
    while stremed < len(sound):
        chunk = sound.read(CHUNK_SIZE, dtype="float32")
        if len(chunk) == 0:
            break

        input_device_stream.write(chunk * 0.5)
        output_device_stream.write(chunk * 0.5)

        stremed += CHUNK_SIZE


def main():
    filename = "./src/sounds/foi-quando-gyro-finalmente-entendeu.mp3"
    sound = sf.SoundFile(filename)

    output_device = 12
    thread = threading.Thread(target=play_on_device, args=(output_device, sound))

    thread.start()
    thread.join()


if __name__ == "__main__":
    main()
