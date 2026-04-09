import asyncio
import argparse

from core.homepage import visit_homepage
from core.session import SESSION
from core.rate_limiter import RateLimiter
from mysterious_passages.the_door_echoed_steps import solve_echoed_steps
from mysterious_passages.the_clockwork_door import solve_clockwork_door
from mysterious_passages.the_exiled_doors import solve_exiled_door, FRESH_SESSION
from curious_reflections.the_fractured_mirror import solve_fractured_mirror
from curious_reflections.the_silver_veil import solve_silver_veil
from curious_reflections.the_mirror_gaze import solve_mirrored_gaze
from shattered_thresholds.the_sleeping_vault import solve_sleeping_vault
from shattered_thresholds.the_verity_gate import solve_verity_gate


async def run_solvers(limiter: RateLimiter, semaphore: asyncio.Semaphore):
    solvers = [
        solve_echoed_steps,
        solve_clockwork_door,
        solve_exiled_door,
        solve_fractured_mirror,
        solve_silver_veil,
        solve_mirrored_gaze,
        solve_sleeping_vault,
        solve_verity_gate,
    ]

    async def run_one(solver):
        async with semaphore:
            await limiter.acquire()
            await solver()

    await asyncio.gather(*[run_one(s) for s in solvers])


async def main(rps: float, concurrency: int):
    print(f"Starting BO7 challenge solver  [rps={rps}  concurrency={concurrency}]\n")

    await visit_homepage()

    limiter = RateLimiter(rps)
    semaphore = asyncio.Semaphore(concurrency)

    await run_solvers(limiter, semaphore)

    await SESSION.close()
    await FRESH_SESSION.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BO7 challenge solver")
    parser.add_argument(
        "--rps",
        type=float,
        default=10.0,
        help="Maximum requests per second across all solvers (default: 10)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=8,
        help="Maximum number of puzzle solvers running concurrently (default: 8)",
    )
    args = parser.parse_args()

    asyncio.run(main(rps=args.rps, concurrency=args.concurrency))
