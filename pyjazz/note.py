class Note:
    __slots__ = "pitch", "position", "duration", "volume"
    def __init__(self, pitch: int,  position: float, duration: float, volume: int=100) -> None:
        self.pitch = pitch
        self.duration = duration
        self.position = position
        self.volume = volume

    def transpose(self, interval: int) -> None:
        self.pitch += interval

    def move(self, interval: int) -> None:
        self.position += interval

    def stretch(self, scale_factor: float) -> None:
        self.duration *= scale_factor