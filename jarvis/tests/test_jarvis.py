from jarvis import Jarvis, JarvisState


def test_jarvis_starts_in_stopped_state() -> None:
    jarvis = Jarvis()

    assert jarvis.status() == JarvisState.STOPPED


def test_jarvis_can_start() -> None:
    jarvis = Jarvis()

    assert jarvis.start() == JarvisState.RUNNING
    assert jarvis.status() == JarvisState.RUNNING


def test_jarvis_can_stop() -> None:
    jarvis = Jarvis()

    jarvis.start()

    assert jarvis.stop() == JarvisState.STOPPED
    assert jarvis.status() == JarvisState.STOPPED
