from core.homepage import get_bo7_homepage, extract_mysterious_value
from core.thumbmark import send_thumbmark
from core.session import SESSION


def solve_echoed_steps():

    homepage_html = get_bo7_homepage()

    mysterious = extract_mysterious_value(homepage_html)

    send_thumbmark(mysterious, "https://bo7.online/")

    door = SESSION.get(
        "https://bo7.online/the_door_of_echoed_steps",
        headers={"referer": "https://bo7.online/"}
    )

    door_html = door.text

    mysterious2 = extract_mysterious_value(door_html)

    send_thumbmark(
        mysterious2,
        "https://bo7.online/the_door_of_echoed_steps"
    )

    print("Echoed steps solved")