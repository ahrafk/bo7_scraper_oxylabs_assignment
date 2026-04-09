import asyncio

from core.homepage import visit_homepage
from core.session import SESSION
from mysterious_passages.the_door_echoed_steps import solve_echoed_steps
from mysterious_passages.the_clockwork_door import solve_clockwork_door
from mysterious_passages.the_exiled_doors import solve_exiled_door, FRESH_SESSION
from curious_reflections.the_fractured_mirror import solve_fractured_mirror
from curious_reflections.the_silver_veil import solve_silver_veil
from curious_reflections.the_mirror_gaze import solve_mirrored_gaze
from shattered_thresholds.the_sleeping_vault import solve_sleeping_vault
from shattered_thresholds.the_verity_gate import solve_verity_gate


async def main():
    print("Starting BO7 challenge solver\n")

    await visit_homepage()

    await asyncio.gather(
        solve_echoed_steps(),
        solve_clockwork_door(),
        solve_exiled_door(),
        solve_fractured_mirror(),
        solve_silver_veil(),
        solve_mirrored_gaze(),
        solve_sleeping_vault(),
        solve_verity_gate(),
    )

    await SESSION.close()
    await FRESH_SESSION.close()


if __name__ == "__main__":
    asyncio.run(main())
