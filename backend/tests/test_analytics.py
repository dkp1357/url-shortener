# test_analytics.py
def test_top_urls(base_url, session, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = session.get(f"{base_url}/analytics/top/", headers=headers, params={"limit": 5})
    assert r.status_code == 200


def test_click_timeline(base_url, session, short_url):
    code = short_url["short_code"]
    r = session.get(f"{base_url}/analytics/{code}/timeline/")
    assert r.status_code == 200


def test_device_stats(base_url, session, short_url):
    code = short_url["short_code"]
    r = session.get(f"{base_url}/analytics/{code}/devices/")
    assert r.status_code == 200