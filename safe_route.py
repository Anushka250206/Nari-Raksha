import heapq
from db import get_connection

def get_location_graph():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT l1.id, l2.id,
        ST_Distance_Sphere(
            POINT(l1.longitude, l1.latitude),
            POINT(l2.longitude, l2.latitude)
        ) AS distance,
        IFNULL(d.danger_score, 0)
        FROM locations l1
        JOIN locations l2 ON l1.id != l2.id
        LEFT JOIN location_danger d ON l2.id = d.location_id
    """)

    graph = {}
    for s, d, dist, danger in cursor.fetchall():
        # distance + danger penalty (research-style weighted risk)
        weight = float(dist) + (float(danger) * 500)
        graph.setdefault(s, []).append((d, weight))

    conn.close()
    return graph


def dijkstra(graph, start, end):
    pq = [(0, start)]
    dist = {node: float('inf') for node in graph}
    prev = {}
    dist[start] = 0

    while pq:
        cd, u = heapq.heappop(pq)
        if u == end:
            break

        for v, w in graph.get(u, []):
            nd = cd + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    path = []
    cur = end
    while cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()

    return path, dist[end]
