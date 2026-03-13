# test_redirect.py
import time


def test_redirect(base_url, session, short_url):
    code = short_url["short_code"]
    r = session.get(
        f"{base_url}/r/{code}/",
        allow_redirects=False
    )
    assert r.status_code == 307


def test_redirect_multiple_clicks(base_url, session, short_url):
    code = short_url["short_code"]

    for _ in range(5):
        r = session.get(
            f"{base_url}/r/{code}/",
            allow_redirects=False
        )
        assert r.status_code == 307

    time.sleep(2)