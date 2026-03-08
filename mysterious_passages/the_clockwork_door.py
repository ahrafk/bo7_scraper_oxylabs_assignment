from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import send_thumbmark


def solve_clockwork_door():

    # Step 1: homepage
    homepage_html = get_bo7_homepage()

    mysterious = extract_mysterious_value(homepage_html)

    send_thumbmark(
        mysterious,
        "https://bo7.online/"
    )

    # Step 2: open clockwork door
    response = SESSION.get(
        "https://bo7.online/the_clockwork_door",
        headers={
            "referer": "https://bo7.online/"
        }
    )

    door_html = response.text

    mysterious2 = extract_mysterious_value(door_html)

    # Step 3: thumbmark again
    thumb = send_thumbmark(
        mysterious2,
        "https://bo7.online/the_clockwork_door"
    )

    print("Clockwork door status:", thumb.status_code)

    if thumb.status_code == 200:
        print("Clockwork door solved")


if __name__ == "__main__":
    solve_clockwork_door()