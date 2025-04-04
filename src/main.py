import threading
from time import sleep

import sounddevice as sd
import soundfile as sf

stop_event = threading.Event()
stop_event.clear()


def play_on_device(
    device_id: int,
    sound: list,
    samplerate: int,
):
    try:
        with sd.OutputStream(
            device=device_id, samplerate=samplerate, channels=sound.shape[1]
        ) as stream:
            pos = 0
            while pos < len(sound) and not stop_event.is_set():
                chunk_size = 1024
                stream.write(sound[pos : pos + chunk_size])
                pos += chunk_size
    except Exception as e:
        print(f"Erro ao tocar no dispositivo {device_id}: {e}")


def main():
    filename = "./src/sounds/foi-quando-gyro-finalmente-entendeu.mp3"
    data, samplerate = sf.read(filename, dtype="float32")

    sound = data * 0.1

    # fone = 31
    fone = sd.default.device[1]
    microfone = 12

    thread1 = threading.Thread(target=play_on_device, args=(fone, sound, samplerate))
    thread2 = threading.Thread(
        target=play_on_device, args=(microfone, sound, samplerate)
    )

    thread1.start()
    thread2.start()

    sleep(2)

    # stop_event.set()

    thread1.join()
    thread2.join()

    # stop_event.clear()


if __name__ == "__main__":
    main()
