class Note:
    __slots__ = "pitch", "position", "duration", "volume"
    def __init__(self, pitch: int,  position: float, duration: float, volume: int=100) -> None:
        self.pitch = pitch
        self.duration = duration
        self.position = position
        self.volume = volume

    def transpose(self, interval: int) -> None:
        new_pitch = self.pitch + interval
        return Note(new_pitch, self.position, self.duration, self.volume)

    def move(self, interval: int) -> None:
        new_position = self.position + interval
        return Note(self.pitch, new_position, self.duration, self.volume)

    def stretch(self, scale_factor: float) -> None:
        new_duration = self.duration * scale_factor
        return Note(self.pitch, self.position, new_duration, self.volume)