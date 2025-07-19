import pyaudio
import numpy as np
import threading

class Audio:
    def __init__(self, chunk_size=1024, audio_format=pyaudio.paInt16, channels=1, rate=44100):
        self.chunk_size = chunk_size
        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.audio_data = None
        self.running = False
        self.thread = None

    def start_stream(self):
        try:
            self.stream = self.p.open(format=self.audio_format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size,
                                      stream_callback=self._callback)
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.daemon = True
            self.thread.start()
            self.stream.start_stream()
        except OSError as e:
            print(f"Could not open audio stream: {e}")
            self.stream = None

    def _callback(self, in_data, frame_count, time_info, status):
        self.audio_data = np.frombuffer(in_data, dtype=np.int16)
        return (in_data, pyaudio.paContinue)

    def _run(self):
        while self.running and self.stream and self.stream.is_active():
            pass

    def stop_stream(self):
        if self.stream is not None:
            self.running = False
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        if self.thread is not None:
            self.thread.join()
