"""
Shared test setup. pytest loads this file automatically before any test.

Two guards so the test run can never hang:

1. No real internet. Any attempt to open a network connection (for example
   the Open-Meteo weather download) fails at once with an error, and the
   weather endpoint gets a fake forecast. Tests that need weather pass their
   own fake `download` function (see tests/test_weather.py).

2. A time limit per test. If one test takes longer than TEST_TIME_LIMIT
   seconds (e.g. waiting on an endless simulator stream), Python prints where
   every thread is stuck and stops the run, instead of waiting forever.
"""

import faulthandler
import socket
import sys

import pytest

TEST_TIME_LIMIT = 60          # seconds; the slowest test today takes about 5


class NoInternetInTests(RuntimeError):
    pass


LOCAL_HOSTS = ("127.0.0.1", "::1", "localhost")
_real_connect = socket.socket.connect


def _blocked(*args, **kwargs):
    raise NoInternetInTests("Tests must not use the real internet. Pass a fake download function instead.")


def _local_only_connect(sock, address):
    # asyncio on Windows connects two local sockets to itself; that must keep working.
    host = address[0] if isinstance(address, tuple) else address
    if host not in LOCAL_HOSTS:
        _blocked()
    return _real_connect(sock, address)


@pytest.fixture(autouse=True)
def no_internet(monkeypatch):
    # FastAPI's TestClient calls the app directly, without sockets, so this
    # only blocks real network traffic.
    monkeypatch.setattr(socket.socket, "connect", _local_only_connect)
    monkeypatch.setattr("urllib.request.urlopen", _blocked)


@pytest.fixture(autouse=True)
def no_real_ai(monkeypatch):
    # The assistant must never call a real AI in tests: no key = no provider.
    # Tests that need replies use a fake provider (see tests/test_assistant.py).
    for name in ("ASSISTANT_API_KEY", "ASSISTANT_PROVIDER", "ASSISTANT_MODEL", "ASSISTANT_BASE_URL"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture(autouse=True)
def fake_weather_cache(monkeypatch, tmp_path):
    # Never read or overwrite the real saved forecast in data/.
    import backend.weather as weather
    defaults = list(weather.tonight_crash_risk.__defaults__)
    defaults[2] = tmp_path / "weather_cache.json"           # cache_file
    monkeypatch.setattr(weather.tonight_crash_risk, "__defaults__", tuple(defaults))


@pytest.fixture(autouse=True)
def fresh_request_limits():
    # Each test starts with empty rate-limit counts (backend/security.py).
    import backend.main as main
    main.request_limiter.clear()


@pytest.fixture(autouse=True)
def time_limit():
    faulthandler.dump_traceback_later(TEST_TIME_LIMIT, exit=True, file=sys.stderr)
    yield
    faulthandler.cancel_dump_traceback_later()
