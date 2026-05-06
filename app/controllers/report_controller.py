import math
import networkx as nx
import igraph as ig
import leidenalg

from app.database import get_neo4j_session


def safe_int(value):
    try:
        return int(value or 0)
    except Exception:
        return 0


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

def get_dashboard_summary():
    query = """
    MATCH (u:FirebaseUser)
    WITH count(u) AS total_new_users

    MATCH (k:FirebaseKawanSS)
    WHERE k.isDeleted = false OR k.isDeleted IS NULL
    WITH total_new_users,
         count(k) AS total_kawanss_posts

    MATCH (i:FirebaseInfoss)
    WHERE i.isDeleted = false OR i.isDeleted IS NULL
    WITH total_new_users,
         total_kawanss_posts,
         count(i) AS total_infoss_posts

    MATCH (igp:InstagramPost)
    WITH total_new_users,
         total_kawanss_posts,
         total_infoss_posts,
         count(igp) AS total_instagram_posts

    MATCH (igu:InstagramUser)
    WITH total_new_users,
         total_kawanss_posts,
         total_infoss_posts,
         total_instagram_posts,
         count(igu) AS total_instagram_users

    MATCH (c)
    WHERE c:FirebaseKawanSSComment
       OR c:FirebaseInfossComment
       OR c:InstagramComment
    WITH total_new_users,
         total_kawanss_posts,
         total_infoss_posts,
         total_instagram_posts,
         total_instagram_users,
         count(c) AS total_comments

    MATCH (l)
    WHERE l:FirebaseLike
       OR l:InstagramLike
    WITH total_new_users,
         total_kawanss_posts,
         total_infoss_posts,
         total_instagram_posts,
         total_instagram_users,
         total_comments,
         count(l) AS total_likes

    RETURN {
        total_new_users: total_new_users,
        total_kawanss_posts: total_kawanss_posts,
        total_infoss_posts: total_infoss_posts,
        total_instagram_posts: total_instagram_posts,
        total_instagram_users: total_instagram_users,
        total_comments: total_comments,
        total_likes: total_likes
    } AS dashboard
    """

    with get_neo4j_session() as session:
        result = session.run(query).single()

    return {
        "status": "success",
        "data": result["dashboard"] if result else {
            "total_new_users": 0,
            "total_kawanss_posts": 0,
            "total_infoss_posts": 0,
            "total_instagram_posts": 0,
            "total_instagram_users": 0,
            "total_comments": 0,
            "total_likes": 0
        }
    }


# ============================================================
# INSTAGRAM PROFILE
# ============================================================

def get_instagram_profile():
    query = """
    MATCH (p:InstaProfile)
    RETURN {
        id: p.id,
        username: p.username,
        name: p.name,
        biography: p.biography,
        followers_count: p.followers_count,
        follows_count: p.follows_count,
        media_count: p.media_count,
        profile_picture_url: p.profile_picture_url
    } AS profile
    LIMIT 1
    """

    with get_neo4j_session() as session:
        result = session.run(query).single()

    return {
        "status": "success",
        "data": result["profile"] if result else None
    }


# ============================================================
# TOP CONTENT
# ============================================================

def get_top_content(source: str = "app", limit: int = 10):
    source = source.lower().strip()

    if source == "instagram":
        return get_top_instagram_content(limit)

    return get_top_app_content(limit)


def get_top_app_content(limit: int):
    query = """
    MATCH (p)
    WHERE (
        p:FirebaseKawanSS OR
        p:FirebaseInfoss
    )
    AND (p.isDeleted = false OR p.isDeleted IS NULL)
    RETURN p.id AS id,
           labels(p)[0] AS type,
           coalesce(p.judul, p.title, p.deskripsi, 'Untitled') AS title,
           coalesce(p.deskripsi, p.detail, '') AS description,
           coalesce(p.uploadDate, p.createdAt, '') AS uploadDate,
           coalesce(p.jumlahView, 0) AS views,
           coalesce(p.jumlahLike, 0) AS likes,
           coalesce(p.jumlahComment, 0) AS comments,
           coalesce(p.jumlahShare, 0) AS shares,
           coalesce(p.jumlahLike, 0) AS score
    ORDER BY likes DESC, comments DESC, views DESC
    LIMIT $limit
    """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    data = []
    for row in records:
        data.append({
            "id": row["id"],
            "type": row["type"],
            "title": row["title"],
            "description": row["description"],
            "uploadDate": row["uploadDate"],
            "views": safe_int(row["views"]),
            "likes": safe_int(row["likes"]),
            "comments": safe_int(row["comments"]),
            "shares": safe_int(row["shares"]),
            "score": safe_int(row["score"]),
            "sort_by": "likes"
        })

    return {
        "status": "success",
        "source": "app",
        "sort_by": "likes",
        "data": data
    }

def get_top_instagram_content(limit: int):
    query = """
    MATCH (p:InstagramPost)
    RETURN p.id AS id,
           p.caption AS caption,
           p.permalink AS permalink,
           p.timestamp AS timestamp,
           p.media_type AS media_type,
           coalesce(p.view_count, 0) AS views,
           coalesce(p.like_count, 0) AS likes,
           coalesce(p.comments_count, 0) AS comments,
           coalesce(p.share_count, 0) AS shares,
           coalesce(p.like_count, 0) AS score
    ORDER BY likes DESC, comments DESC, views DESC
    LIMIT $limit
    """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    data = []
    for row in records:
        data.append({
            "id": row["id"],
            "caption": row["caption"],
            "permalink": row["permalink"],
            "timestamp": row["timestamp"],
            "media_type": row["media_type"],
            "views": safe_int(row["views"]),
            "likes": safe_int(row["likes"]),
            "comments": safe_int(row["comments"]),
            "shares": safe_int(row["shares"]),
            "score": safe_int(row["score"]),
            "sort_by": "likes"
        })

    return {
        "status": "success",
        "source": "instagram",
        "sort_by": "likes",
        "data": data
    }
# ============================================================
# TOP HASHTAGS
# ============================================================

def get_top_hashtags(source: str = "app", limit: int = 10):
    source = source.lower().strip()

    if source == "instagram":
        query = """
        MATCH (p:InstagramPost)-[:HAS_HASHTAG]->(h:Hashtag)
        RETURN h.name AS hashtag,
               count(p) AS total_posts,
               sum(coalesce(p.like_count, 0)) AS total_likes,
               sum(coalesce(p.comments_count, 0)) AS total_comments
        ORDER BY total_posts DESC, total_likes DESC
        LIMIT $limit
        """
    else:
        query = """
        MATCH (p)-[:HAS_HASHTAG]->(h:Hashtag)
        WHERE p:FirebaseKawanSS OR p:FirebaseInfoss
        RETURN h.name AS hashtag,
               count(p) AS total_posts,
               sum(coalesce(p.jumlahLike, 0)) AS total_likes,
               sum(coalesce(p.jumlahComment, 0)) AS total_comments
        ORDER BY total_posts DESC, total_likes DESC
        LIMIT $limit
        """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    data = []
    for row in records:
        data.append({
            "hashtag": f"#{row['hashtag']}",
            "total_posts": safe_int(row["total_posts"]),
            "total_likes": safe_int(row["total_likes"]),
            "total_comments": safe_int(row["total_comments"])
        })

    return {
        "status": "success",
        "source": source,
        "data": data
    }


# ============================================================
# NETWORK ANALYSIS
# CENTRALITY + LEIDEN + GEODESIC
# ============================================================

def get_network_analysis(source: str = "app", limit: int = 1200, top: int = 10):
    source = source.lower().strip()

    if source not in ["app", "instagram"]:
        return {
            "status": "error",
            "message": "Invalid source. Use 'app' or 'instagram'."
        }

    records = _fetch_user_graph_edges(source=source, limit=limit)
    graph, node_labels = _build_networkx_graph(records)

    if graph.number_of_nodes() == 0:
        return {
            "status": "success",
            "source": source,
            "data": {
                "summary": {
                    "total_nodes": 0,
                    "total_edges": 0,
                    "is_empty": True
                },
                "centrality": {
                    "degree": [],
                    "eigenvector": [],
                    "closeness": [],
                    "betweenness": []
                },
                "leiden": {
                    "total_communities": 0,
                    "communities": []
                },
                "geodesic_paths": []
            }
        }

    centrality = _calculate_centrality(graph, node_labels, top)
    leiden = _calculate_leiden_communities(graph, node_labels, top)
    geodesic_paths = _calculate_geodesic_paths(graph, node_labels, top)

    return {
        "status": "success",
        "source": source,
        "data": {
            "summary": {
                "total_nodes": graph.number_of_nodes(),
                "total_edges": graph.number_of_edges(),
                "is_empty": False
            },
            "centrality": centrality,
            "leiden": leiden,
            "geodesic_paths": geodesic_paths
        }
    }


def _fetch_user_graph_edges(source: str, limit: int):
    if source == "instagram":
        query = """
        MATCH (u1:InstagramUser)-[:WROTE_IG]->(c1:InstagramComment)-[:COMMENTED_ON_IG]->(p:InstagramPost)
        MATCH (u2:InstagramUser)-[:WROTE_IG]->(c2:InstagramComment)-[:COMMENTED_ON_IG]->(p)
        WHERE u1.username < u2.username
        RETURN u1.username AS source,
               coalesce(u1.full_name, u1.username) AS source_label,
               u2.username AS target,
               coalesce(u2.full_name, u2.username) AS target_label,
               count(DISTINCT p) AS weight
        ORDER BY weight DESC
        LIMIT $limit
        """
    else:
        query = """
        MATCH (u1:FirebaseUser)-[:WROTE_FB]->(c1)-[:COMMENTED_ON_FB]->(p)
        MATCH (u2:FirebaseUser)-[:WROTE_FB]->(c2)-[:COMMENTED_ON_FB]->(p)
        WHERE u1.id < u2.id
        RETURN u1.id AS source,
               coalesce(u1.nama, u1.username, u1.id) AS source_label,
               u2.id AS target,
               coalesce(u2.nama, u2.username, u2.id) AS target_label,
               count(DISTINCT p) AS weight
        ORDER BY weight DESC
        LIMIT $limit
        """

    with get_neo4j_session() as session:
        return session.run(query, limit=limit).data()


def _build_networkx_graph(records):
    graph = nx.Graph()
    node_labels = {}

    for row in records:
        source = str(row["source"])
        target = str(row["target"])
        source_label = str(row["source_label"])
        target_label = str(row["target_label"])
        weight = float(row["weight"] or 1)

        node_labels[source] = source_label
        node_labels[target] = target_label

        distance = 1.0 / max(weight, 1.0)

        if graph.has_edge(source, target):
            graph[source][target]["weight"] += weight
            graph[source][target]["distance"] = 1.0 / graph[source][target]["weight"]
        else:
            graph.add_edge(
                source,
                target,
                weight=weight,
                distance=distance
            )

    return graph, node_labels


def _calculate_centrality(graph, node_labels, top):
    degree = nx.degree_centrality(graph)

    try:
        eigenvector = nx.eigenvector_centrality(
            graph,
            max_iter=1000,
            weight="weight"
        )
    except Exception:
        eigenvector = {node: 0.0 for node in graph.nodes()}

    try:
        closeness = nx.closeness_centrality(
            graph,
            distance="distance"
        )
    except Exception:
        closeness = {node: 0.0 for node in graph.nodes()}

    try:
        if graph.number_of_nodes() > 400:
            betweenness = nx.betweenness_centrality(
                graph,
                k=min(200, graph.number_of_nodes()),
                weight="distance",
                seed=42
            )
        else:
            betweenness = nx.betweenness_centrality(
                graph,
                weight="distance"
            )
    except Exception:
        betweenness = {node: 0.0 for node in graph.nodes()}

    return {
        "degree": _top_centrality_items(degree, node_labels, top),
        "eigenvector": _top_centrality_items(eigenvector, node_labels, top),
        "closeness": _top_centrality_items(closeness, node_labels, top),
        "betweenness": _top_centrality_items(betweenness, node_labels, top),
    }


def _top_centrality_items(scores, node_labels, top):
    sorted_items = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:top]

    result = []

    for index, item in enumerate(sorted_items, start=1):
        node_id, score = item

        result.append({
            "rank": index,
            "id": node_id,
            "label": node_labels.get(node_id, node_id),
            "score": round(float(score), 6)
        })

    return result


def _calculate_leiden_communities(graph, node_labels, top):
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return {
            "total_communities": 0,
            "communities": []
        }

    edge_tuples = []

    for source, target, data in graph.edges(data=True):
        edge_tuples.append((
            source,
            target,
            float(data.get("weight", 1))
        ))

    ig_graph = ig.Graph.TupleList(
        edge_tuples,
        directed=False,
        weights=True,
        vertex_name_attr="name"
    )

    partition = leidenalg.find_partition(
        ig_graph,
        leidenalg.RBConfigurationVertexPartition,
        weights="weight",
        seed=42
    )

    communities = []

    for community_index, community in enumerate(partition):
        members = []

        for vertex_index in community:
            node_id = ig_graph.vs[vertex_index]["name"]
            members.append({
                "id": node_id,
                "label": node_labels.get(node_id, node_id)
            })

        communities.append({
            "community_id": community_index,
            "size": len(members),
            "members": members[:20]
        })

    communities.sort(key=lambda item: item["size"], reverse=True)

    for index, item in enumerate(communities, start=1):
        item["rank"] = index

    return {
        "total_communities": len(communities),
        "communities": communities[:top]
    }


def _calculate_geodesic_paths(graph, node_labels, top):
    if graph.number_of_nodes() < 2:
        return []

    degree_pairs = sorted(
        graph.degree,
        key=lambda item: item[1],
        reverse=True
    )

    candidate_nodes = [
        node for node, _ in degree_pairs[:min(25, len(degree_pairs))]
    ]

    paths = []

    for i in range(len(candidate_nodes)):
        for j in range(i + 1, len(candidate_nodes)):
            source = candidate_nodes[i]
            target = candidate_nodes[j]

            try:
                path = nx.shortest_path(
                    graph,
                    source=source,
                    target=target,
                    weight="distance"
                )

                if len(path) < 2:
                    continue

                path_edges = []
                total_distance = 0.0
                total_weight = 0.0

                for step in range(len(path) - 1):
                    a = path[step]
                    b = path[step + 1]
                    edge_data = graph.get_edge_data(a, b, default={})

                    weight = float(edge_data.get("weight", 1))
                    distance = float(edge_data.get("distance", 1))

                    total_weight += weight
                    total_distance += distance

                    path_edges.append({
                        "source": a,
                        "target": b,
                        "source_label": node_labels.get(a, a),
                        "target_label": node_labels.get(b, b),
                        "weight": weight
                    })

                paths.append({
                    "source": source,
                    "source_label": node_labels.get(source, source),
                    "target": target,
                    "target_label": node_labels.get(target, target),
                    "hops": len(path) - 1,
                    "total_weight": round(total_weight, 4),
                    "total_distance": round(total_distance, 6),
                    "path": [
                        {
                            "id": node_id,
                            "label": node_labels.get(node_id, node_id)
                        }
                        for node_id in path
                    ],
                    "edges": path_edges,
                    "path_details": " → ".join(
                        node_labels.get(node_id, node_id)
                        for node_id in path
                    )
                })

            except nx.NetworkXNoPath:
                continue
            except Exception:
                continue

    paths.sort(
        key=lambda item: (
            item["hops"],
            item["total_weight"]
        ),
        reverse=True
    )

    result = []

    for index, path in enumerate(paths[:top], start=1):
        path["rank"] = index
        result.append(path)

    return result