"""
Humanized Interaction Mechanics for PhantomVault.
Generates organic Bézier mouse paths, realistic keystroke hold-down durations, and high-speed execution modes.
"""
import asyncio
import math
import random
from typing import List, Tuple, Any


def cubic_bezier_point(t: float, p0: Tuple[float, float], p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> Tuple[float, float]:
    """Calculate point on cubic bezier curve at parameter t in [0, 1]."""
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t

    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    return (x, y)


def generate_bezier_trajectory(start: Tuple[float, float], target: Tuple[float, float], num_points: int = 20) -> List[Tuple[float, float]]:
    """
    Constructs an organic curved mouse path with human-like overshoot and deceleration.
    """
    dx = target[0] - start[0]
    dy = target[1] - start[1]
    dist = math.hypot(dx, dy)

    deviation = min(dist * 0.3, 80.0)
    dev_x1 = (random.random() - 0.5) * deviation
    dev_y1 = (random.random() - 0.5) * deviation
    dev_x2 = (random.random() - 0.5) * deviation
    dev_y2 = (random.random() - 0.5) * deviation

    p0 = start
    p1 = (start[0] + dx * 0.3 + dev_x1, start[1] + dy * 0.3 + dev_y1)
    p2 = (start[0] + dx * 0.7 + dev_x2, start[1] + dy * 0.7 + dev_y2)
    p3 = target

    trajectory: List[Tuple[float, float]] = []
    for i in range(num_points):
        t = i / (num_points - 1)
        smooth_t = t * t * (3 - 2 * t)
        point = cubic_bezier_point(smooth_t, p0, p1, p2, p3)
        if 0 < i < num_points - 1:
            jitter_x = (random.random() - 0.5) * 0.6
            jitter_y = (random.random() - 0.5) * 0.6
        else:
            jitter_x = 0.0
            jitter_y = 0.0
        trajectory.append((round(point[0] + jitter_x, 1), round(point[1] + jitter_y, 1)))

    return trajectory


class Humanizer:
    """
    Async helpers for performing undetectable human actions on Playwright pages
    with built-in high-speed throughput modes.
    """

    @staticmethod
    async def move_mouse_async(
        page: Any,
        target_x: float,
        target_y: float,
        start_x: float = 100.0,
        start_y: float = 100.0,
        steps: int = 15,
        fast: bool = False
    ):
        """Asynchronously glide mouse to target coordinates along a realistic Bézier curve."""
        point_count = 8 if fast else steps
        path = generate_bezier_trajectory((start_x, start_y), (target_x, target_y), num_points=point_count)
        step_sleep = (0.002, 0.006) if fast else (0.006, 0.016)
        
        for x, y in path:
            await page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(*step_sleep))

    @staticmethod
    async def click_element_async(page: Any, selector: str, fast: bool = False):
        """Finds element bounding box, glides cursor organically, and clicks with realistic hold duration."""
        element = await page.wait_for_selector(selector, state="visible")
        box = await element.bounding_box()
        if not box:
            await page.click(selector)
            return

        target_x = box["x"] + box["width"] * random.uniform(0.35, 0.65)
        target_y = box["y"] + box["height"] * random.uniform(0.35, 0.65)

        await Humanizer.move_mouse_async(page, target_x, target_y, fast=fast)
        
        pre_click_delay = random.uniform(0.02, 0.05) if fast else random.uniform(0.04, 0.12)
        await asyncio.sleep(pre_click_delay)

        # Human hold-down duration (Akamai / DataDome telemetry check)
        await page.mouse.down()
        hold_time = random.uniform(0.03, 0.06) if fast else random.uniform(0.05, 0.09)
        await asyncio.sleep(hold_time)
        await page.mouse.up()

    @staticmethod
    async def type_text_async(page: Any, selector: str, text: str, wpm: int = 85, fast: bool = False):
        """
        Simulates human typing with authentic down/up hold-down durations (Akamai sensor_data)
        and supports ultra-fast execution mode.
        """
        await Humanizer.click_element_async(page, selector, fast=fast)
        
        if fast:
            base_delay = 0.015
            hold_range = (0.01, 0.025)
        else:
            base_delay = 60.0 / (wpm * 5.0)
            hold_range = (0.035, 0.075)

        for char in text:
            try:
                # Authentic keydown -> hold -> keyup
                await page.keyboard.down(char)
                await asyncio.sleep(random.uniform(*hold_range))
                await page.keyboard.up(char)
            except Exception:
                await page.keyboard.press(char)

            if not fast:
                delay = max(0.01, random.gauss(base_delay, base_delay * 0.3))
                if char in " .,?!":
                    delay += random.uniform(0.05, 0.15)
                await asyncio.sleep(delay)
            else:
                await asyncio.sleep(random.uniform(0.005, 0.015))

    @staticmethod
    async def smooth_scroll_async(page: Any, delta_y: int, steps: int = 6, fast: bool = False):
        """Smooth human-like scrolling with easing."""
        num_steps = 4 if fast else steps
        step_delta = delta_y / num_steps
        step_sleep = (0.01, 0.03) if fast else (0.03, 0.06)
        
        for _ in range(num_steps):
            jitter = step_delta * random.uniform(0.85, 1.15)
            await page.mouse.wheel(0, jitter)
            await asyncio.sleep(random.uniform(*step_sleep))
