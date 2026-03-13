from user_agents import parse

def parse_device(user_agent_string):
    ua = parse(user_agent_string)

    device_type = "mobile" if ua.is_mobile else "tablet" if ua.is_tablet else "desktop"

    return {
        "device_type": device_type,
        "browser": ua.browser.family,
        "os": ua.os.family
    }