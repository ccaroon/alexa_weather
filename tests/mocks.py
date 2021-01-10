import json
################################################################################
class MockResponse:
    def __init__(self, status, content):
        self.status_code = status
        self.content = content
        self.ok = False
        if status < 300:
            self.ok = True

    def json(self):
        return json.loads(self.content)
################################################################################
