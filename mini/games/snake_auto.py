"""Text snake on a small grid. The snake steers itself greedily toward food (always auto)."""
import random
from collections import deque

W, H = 12, 8


def step(snake: deque, food: tuple[int, int]):
    hx, hy = snake[0]
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    moves.sort(key=lambda m: abs(hx + m[0] - food[0]) + abs(hy + m[1] - food[1]))
    for dx, dy in moves:
        nx, ny = hx + dx, hy + dy
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in list(snake)[:-1]:
            return nx, ny
    return None


def main() -> None:
    random.seed(7)
    snake = deque([(3, 3)])
    food = (8, 5)
    for t in range(60):
        nxt = step(snake, food)
        if nxt is None:
            print("snake trapped at length", len(snake))
            return
        snake.appendleft(nxt)
        if nxt == food:
            free = [(x, y) for x in range(W) for y in range(H) if (x, y) not in snake]
            food = random.choice(free)
        else:
            snake.pop()
    for y in range(H):
        print("".join("O" if (x, y) == snake[0] else "o" if (x, y) in snake else "*" if (x, y) == food else "." for x in range(W)))
    print("length", len(snake))


if __name__ == "__main__":
    main()
