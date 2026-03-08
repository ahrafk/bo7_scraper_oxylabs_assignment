from core.session import SESSION
from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import send_thumbmark


def solve_clockwork_door():

    homepage_html = get_bo7_homepage()

    mysterious = extract_mysterious_value(homepage_html)

    send_thumbmark(
        mysterious,
        "https://bo7.online/"
    )

    response = SESSION.get(
        "https://bo7.online/the_clockwork_door",
        headers={
            "referer": "https://bo7.online/"
        }
    )

    door_html = response.text

    mysterious2 = extract_mysterious_value(door_html)

    thumb = send_thumbmark(
        mysterious2,
        "https://bo7.online/the_clockwork_door"
    )

    print("Clockwork door status:", thumb.status_code)

    if thumb.status_code == 200:
        with open("test_results/clockwork_door_result.html", "w") as f:
            f.write(thumb.text)
            f.close()
        print("Clockwork door solved")


if __name__ == "__main__":
    solve_clockwork_door()