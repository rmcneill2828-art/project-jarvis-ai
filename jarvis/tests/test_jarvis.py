from jarvis.core.jarvis import Jarvis


def test_jarvis_starts() -> None:
    jarvis = Jarvis()

    assert jarvis.start() == "JARVIS initialised"
