"""Doppler shift for a moving source/observer in air."""
SPEED_OF_SOUND = 343.0


def observed_frequency(f: float, v_source: float = 0.0, v_observer: float = 0.0,
                       c: float = SPEED_OF_SOUND) -> float:
    """Positive v_source = moving toward observer; positive v_observer = moving toward source."""
    return f * (c + v_observer) / (c - v_source)


def main() -> None:
    f = 440.0
    for v in (0, 10, 30, 60):
        print(f"ambulance {v:>2} m/s: approaching {observed_frequency(f, v):7.2f} Hz, "
              f"receding {observed_frequency(f, -v):7.2f} Hz")


if __name__ == "__main__":
    main()
