import heapq

# Кількість вершин графа
N = 8

# Ребра графа варіанта №15 (u, v, вага)
EDGES = [
    (1, 2, 8), (1, 3, 2), (1, 4, 4), (1, 5, 3),
    (2, 5, 6), (2, 6, 3), (3, 4, 6), (3, 6, 7),
    (3, 8, 4), (4, 5, 1), (5, 7, 4), (6, 7, 3),
    (6, 8, 1), (7, 8, 5)
]

def build_graph(n, edges):
    """Побудова списку суміжності графа."""
    graph = {v: [] for v in range(1, n + 1)}

    # Граф неорієнтований
    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    # Сортуємо сусідів за номерами вершин
    for v in graph:
        graph[v].sort()

    return graph

def fmt(x):
    """Відображення нескінченності."""
    return "∞" if x == float("inf") else str(x)

def show_array(array):
    """Виведення масиву для вершин 1...8."""
    return "[" + ", ".join(map(fmt, array[1:])) + "]"

def show_queue(dist, visited):
    """Виведення актуального стану черги."""
    queue = sorted(
        (dist[v], v)
        for v in range(1, len(dist))
        if not visited[v]
    )

    return "{" + ", ".join(
        f"({v},{fmt(d)})" for d, v in queue
    ) + "}"

def reconstruct_path(pred, source, target):
    """Відновлення найкоротшого шляху."""
    path = []
    v = target

    while v != -1:
        path.append(v)

        if v == source:
            return path[::-1]
        v = pred[v]

    return []

def dijkstra(graph, start):
    """
    Алгоритм Дейкстри.
    Вхідні дані: граф, початкова вершина.
    Вихідні дані: dist, pred.
    """
    n = len(graph)
    inf = float("inf")

    # Ініціалізація масивів
    dist = [inf] * (n + 1)
    pred = [-1] * (n + 1)
    visited = [False] * (n + 1)
    dist[start] = 0

    # Створення черги з пріоритетом
    pq = [(dist[v], v) for v in range(1, n + 1)]
    heapq.heapify(pq)

    print("--- Ініціалізація ---")
    print("dist =", show_array(dist))
    print("pred =", show_array(pred))
    print("pq =", show_queue(dist, visited))

    step = 0

    # Основний цикл алгоритму
    while pq:
        d, u = heapq.heappop(pq)

        # Пропускаємо застарілі записи
        if visited[u] or d != dist[u]:
            continue

        if d == inf:
            break

        # Позначаємо вершину обробленою
        visited[u] = True
        step += 1

        print(f"\nКрок {step}. "
              f"Обробка вершини {u}; dist = {fmt(d)}")

        # Переглядаємо суміжні вершини
        for v, weight in graph[u]:

            if visited[v]:
                continue

            # Обчислюємо нову відстань
            new_d = dist[u] + weight

            # Перевірка можливості релаксації
            if new_d < dist[v]:
                print(
                    f"  ({u},{v}): {fmt(dist[v])} > "
                    f"{fmt(dist[u])} + {weight} = "
                    f"{fmt(new_d)} → оновлення"
                )

                # Оновлення відстані та попередника
                dist[v] = new_d
                pred[v] = u

                # Додавання нового пріоритету
                heapq.heappush(pq, (new_d, v))

            else:
                print(
                    f"  ({u},{v}): {fmt(dist[v])} > "
                    f"{fmt(dist[u])} + {weight} = "
                    f"{fmt(new_d)} → ні"
                )

        # Поточний стан алгоритму
        print("dist =", show_array(dist))
        print("pred =", show_array(pred))
        print("pq =", show_queue(dist, visited))
    return dist, pred

# Основна частина програми
graph = build_graph(N, EDGES)

# Початкова вершина
start = 1
dist, pred = dijkstra(graph, start)

# Виведення найкоротших шляхів
print("\n--- Найкоротші шляхи ---")

for v in range(1, N + 1):
    if v == start:
        continue

    path = reconstruct_path(pred, start, v)
    print(
        f"{start} → {v}: "
        + " → ".join(map(str, path))
        + f" | вага = {fmt(dist[v])}"
    )

# Підсумкові результати
print("\n --- Кінцеві масиви ---")
print("dist =", show_array(dist))
print("pred =", show_array(pred))
