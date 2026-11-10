# Кількість вершин графа
N = 8

# Позначення нескінченності
INF = float("inf")

# Ребра графа варіанта №15 (u, v, вага)
EDGES = [
    (1, 2, 8), (1, 3, 2), (1, 4, 4), (1, 5, 3),
    (2, 5, 6), (2, 6, 3), (3, 4, 6), (3, 6, 7),
    (3, 8, 4), (4, 5, 1), (5, 7, 4), (6, 7, 3),
    (6, 8, 1), (7, 8, 5)
]


def build_weight_matrix(n, edges):
    """Побудова початкової матриці ваг W."""

    # Ініціалізація матриці
    W = [[INF] * n for _ in range(n)]

    # Нульові елементи головної діагоналі
    for i in range(n):
        W[i][i] = 0

    # Заповнення матриці вагами ребер
    for u, v, weight in edges:
        W[u - 1][v - 1] = weight
        W[v - 1][u - 1] = weight

    return W


def format_value(value):
    """Відображення нескінченності."""
    return "∞" if value == INF else str(value)


def display_matrix(D, k):
    """Виведення матриці відстаней D(k)."""

    print(f"\n--- Матриця D({k}) ---")

    # Заголовки стовпців
    print("     " + "".join(
        f"{j:>4}" for j in range(1, len(D) + 1)
    ))

    # Виведення рядків матриці
    for i, row in enumerate(D, start=1):
        values = "".join(
            f"{format_value(x):>4}" for x in row
        )
        print(f"{i:>3}  {values}")


def floyd(W):
    """
    Алгоритм Флойда.
    Вхідні дані: матриця ваг W.
    Вихідні дані: матриця найкоротших відстаней D.
    """

    n = len(W)

    # Копіювання початкової матриці
    D = [row[:] for row in W]

    # Початковий стан
    display_matrix(D, 0)

    # Послідовно розглядаємо проміжні вершини
    for k in range(n):

        # Список змінених відстаней
        changes = []

        # Перебираємо початкові вершини
        for i in range(n):

            # Перебираємо кінцеві вершини
            for j in range(n):

                # Перевірка досяжності через k
                if D[i][k] == INF or D[k][j] == INF:
                    continue

                # Довжина шляху через вершину k
                new_distance = D[i][k] + D[k][j]

                # Перевірка можливості скорочення
                if new_distance < D[i][j]:

                    old_distance = D[i][j]

                    # Оновлення найкоротшої відстані
                    D[i][j] = new_distance

                    # Для неорієнтованого графа
                    # виводимо кожну пару один раз
                    if i < j:
                        changes.append((
                            i + 1, j + 1,
                            old_distance, new_distance
                        ))

        # Виведення результатів поточного кроку
        print(f"\nКрок {k + 1}. "
              f"Проміжна вершина k = {k + 1}")

        if changes:
            print("Оновлення відстаней:")

            for u, v, old, new in changes:
                print(
                    f"  d[{u},{v}]: "
                    f"{format_value(old)} -> {new}"
                )
        else:
            print("Оновлень немає.")

        # Матриця після поточної ітерації
        display_matrix(D, k + 1)

    return D

# Основна частина програми
W = build_weight_matrix(N, EDGES)

print("=== Алгоритм Флойда ===")
print("Варіант №15, кількість вершин:", N)

# Побудова матриці найкоротших відстаней
D = floyd(W)

# Підсумковий результат
print("\n --- Кінцева матриця відстаней ---")
display_matrix(D, N)

# Перевірка результату алгоритму Дейкстри
dijkstra_dist = [0, 8, 2, 4, 3, 7, 7, 6]

print("\n--- Порівняння з алгоритмом Дейкстри ---")
print("Дейкстра:", dijkstra_dist)
print("Флойд:   ", D[0])

if D[0] == dijkstra_dist:
    print("Результати повністю збігаються.")
else:
    print("Виявлено розбіжності.")
