import json

from agentic_ai.functions.agents import get_current_weather


class DummyResponse:
    def __init__(self, temp_c):
        self._temp = temp_c

    def json(self):
        return {'current': {'temp_c': self._temp}}


def test_get_current_weather(monkeypatch):
    # monkeypatch requests.get to avoid a real API call
    monkeypatch.setattr('agentic_ai.functions.agents.requests.get', lambda url: DummyResponse(21))

    res = get_current_weather('Tokyo')
    data = json.loads(res)

    assert data['location'] == 'Tokyo'
    assert 'temperature' in data
