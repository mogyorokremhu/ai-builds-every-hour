"""Random weather forecast generator for a week. Usage: python weather.py [days] [seed]"""
import random
import sys

SKY = ["sunny", "cloudy", "rainy", "windy", "foggy", "stormy", "snowy"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
NEXT = {  # simple Markov chain so the weather changes plausibly
    "sunny": ["sunny", "sunny", "cloudy", "windy"],
    "cloudy": ["cloudy", "rainy", "sunny", "foggy"],
    "rainy": ["rainy", "stormy", "cloudy"],
    "windy": ["windy", "cloudy", "sunny"],
    "foggy": ["foggy", "cloudy", "sunny"],
    "stormy": ["rainy", "cloudy", "stormy"],
    "snowy": ["snowy", "cloudy", "foggy"],
}


def forecast(days: int, rng: random.Random) -> list[str]:
    sky = rng.choice(SKY)
    temp = rng.randint(-5, 28)
    out = []
    for i in range(days):
        out.append(f"{DAYS[i % 7]}  {sky:<7} {temp:>3}°C")
        sky = rng.choice(NEXT[sky])
        temp += rng.randint(-4, 4)
        if sky == "snowy" and temp > 1:
            sky = "rainy"
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    rng = random.Random(int(a[1])) if len(a) > 1 else random.Random()
    print("\n".join(forecast(int(a[0]) if a else 7, rng)))
