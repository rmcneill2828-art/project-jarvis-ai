from jarvis import Jarvis, JarvisState


def test_public_api_exports_lifecycle_components() -> None:
    jarvis = Jarvis()

    assert jarvis.status() == JarvisState.STOPPED
