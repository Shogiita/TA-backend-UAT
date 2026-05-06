from app.database import get_neo4j_session


def get_visualization(source: str = "app", mode: int = 1, limit: int = 500):
    source = source.lower().strip()

    if source not in ["app", "instagram"]:
        return {
            "status": "error",
            "message": "Invalid source. Use 'app' or 'instagram'."
        }

    if mode not in [1, 2, 3]:
        return {
            "status": "error",
            "message": "Invalid mode. Use 1, 2, or 3."
        }

    if source == "instagram":
        if mode == 1:
            return get_instagram_user_to_user(limit)
        if mode == 2:
            return get_instagram_user_to_post(limit)
        if mode == 3:
            return get_instagram_post_to_post(limit)

    if mode == 1:
        return get_app_user_to_user(limit)
    if mode == 2:
        return get_app_user_to_post(limit)
    if mode == 3:
        return get_app_post_to_post(limit)


def build_response(source, mode, nodes_map, edges):
    return {
        "status": "success",
        "source": source,
        "mode": mode,
        "data": {
            "nodes": list(nodes_map.values()),
            "edges": edges,
            "summary": {
                "total_nodes": len(nodes_map),
                "total_edges": len(edges)
            }
        }
    }


def get_app_user_to_user(limit: int):
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
        records = session.run(query, limit=limit).data()

    nodes = {}
    edges = []

    for row in records:
        nodes[row["source"]] = {
            "id": row["source"],
            "label": row["source_label"],
            "type": "user",
            "group": "FirebaseUser"
        }

        nodes[row["target"]] = {
            "id": row["target"],
            "label": row["target_label"],
            "type": "user",
            "group": "FirebaseUser"
        }

        edges.append({
            "source": row["source"],
            "target": row["target"],
            "weight": row["weight"],
            "type": "USER_TO_USER"
        })

    return build_response("app", 1, nodes, edges)


def get_app_user_to_post(limit: int):
    query = """
    MATCH (u:FirebaseUser)-[r]->(x)
    WHERE type(r) = 'POSTED_FB'
       OR type(r) = 'LIKED_FB'
       OR type(r) = 'WROTE_FB'
    WITH u, r, x
    OPTIONAL MATCH (x)-[:LIKED_TARGET_FB]->(likedPost)
    OPTIONAL MATCH (x)-[:COMMENTED_ON_FB]->(commentedPost)
    WITH u,
         CASE
           WHEN likedPost IS NOT NULL THEN likedPost
           WHEN commentedPost IS NOT NULL THEN commentedPost
           ELSE x
         END AS post,
         type(r) AS relation_type
    WHERE post:FirebaseKawanSS OR post:FirebaseInfoss
    RETURN u.id AS source,
           coalesce(u.nama, u.username, u.id) AS source_label,
           post.id AS target,
           coalesce(post.judul, post.title, post.deskripsi, post.id) AS target_label,
           labels(post)[0] AS post_type,
           relation_type AS relation_type
    LIMIT $limit
    """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    nodes = {}
    edges = []

    for row in records:
        nodes[row["source"]] = {
            "id": row["source"],
            "label": row["source_label"],
            "type": "user",
            "group": "FirebaseUser"
        }

        nodes[row["target"]] = {
            "id": row["target"],
            "label": row["target_label"],
            "type": "post",
            "group": row["post_type"]
        }

        edges.append({
            "source": row["source"],
            "target": row["target"],
            "weight": 1,
            "type": row["relation_type"]
        })

    return build_response("app", 2, nodes, edges)


def get_app_post_to_post(limit: int):
    query = """
    MATCH (u:FirebaseUser)-[:WROTE_FB]->(c1)-[:COMMENTED_ON_FB]->(p1)
    MATCH (u:FirebaseUser)-[:WROTE_FB]->(c2)-[:COMMENTED_ON_FB]->(p2)
    WHERE id(p1) < id(p2)
      AND (p1:FirebaseKawanSS OR p1:FirebaseInfoss)
      AND (p2:FirebaseKawanSS OR p2:FirebaseInfoss)
    RETURN p1.id AS source,
           coalesce(p1.judul, p1.title, p1.deskripsi, p1.id) AS source_label,
           labels(p1)[0] AS source_group,
           p2.id AS target,
           coalesce(p2.judul, p2.title, p2.deskripsi, p2.id) AS target_label,
           labels(p2)[0] AS target_group,
           count(DISTINCT u) AS weight
    ORDER BY weight DESC
    LIMIT $limit
    """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    nodes = {}
    edges = []

    for row in records:
        nodes[row["source"]] = {
            "id": row["source"],
            "label": row["source_label"],
            "type": "post",
            "group": row["source_group"]
        }

        nodes[row["target"]] = {
            "id": row["target"],
            "label": row["target_label"],
            "type": "post",
            "group": row["target_group"]
        }

        edges.append({
            "source": row["source"],
            "target": row["target"],
            "weight": row["weight"],
            "type": "POST_TO_POST"
        })

    return build_response("app", 3, nodes, edges)


def get_instagram_user_to_user(limit: int):
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

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    nodes = {}
    edges = []

    for row in records:
        nodes[row["source"]] = {
            "id": row["source"],
            "label": row["source_label"],
            "type": "user",
            "group": "InstagramUser"
        }

        nodes[row["target"]] = {
            "id": row["target"],
            "label": row["target_label"],
            "type": "user",
            "group": "InstagramUser"
        }

        edges.append({
            "source": row["source"],
            "target": row["target"],
            "weight": row["weight"],
            "type": "IG_USER_TO_USER"
        })

    return build_response("instagram", 1, nodes, edges)


def get_instagram_user_to_post(limit: int):
    query = """
    MATCH (u:InstagramUser)-[r]->(x)
    WHERE type(r) = 'POSTED_IG'
       OR type(r) = 'WROTE_IG'
       OR type(r) = 'LIKED_IG'
    WITH u, r, x
    OPTIONAL MATCH (x)-[:COMMENTED_ON_IG]->(commentedPost:InstagramPost)
    OPTIONAL MATCH (x)-[:LIKED_TARGET_IG]->(likedPost:InstagramPost)
    WITH u,
         CASE
           WHEN commentedPost IS NOT NULL THEN commentedPost
           WHEN likedPost IS NOT NULL THEN likedPost
           ELSE x
         END AS post,
         type(r) AS relation_type
    WHERE post:InstagramPost
    RETURN u.username AS source,
           coalesce(u.full_name, u.username) AS source_label,
           post.id AS target,
           coalesce(substring(post.caption, 0, 80), post.id) AS target_label,
           relation_type AS relation_type
    LIMIT $limit
    """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    nodes = {}
    edges = []

    for row in records:
        nodes[row["source"]] = {
            "id": row["source"],
            "label": row["source_label"],
            "type": "user",
            "group": "InstagramUser"
        }

        nodes[row["target"]] = {
            "id": row["target"],
            "label": row["target_label"],
            "type": "post",
            "group": "InstagramPost"
        }

        edges.append({
            "source": row["source"],
            "target": row["target"],
            "weight": 1,
            "type": row["relation_type"]
        })

    return build_response("instagram", 2, nodes, edges)


def get_instagram_post_to_post(limit: int):
    query = """
    MATCH (u:InstagramUser)-[:WROTE_IG]->(c1:InstagramComment)-[:COMMENTED_ON_IG]->(p1:InstagramPost)
    MATCH (u:InstagramUser)-[:WROTE_IG]->(c2:InstagramComment)-[:COMMENTED_ON_IG]->(p2:InstagramPost)
    WHERE p1.id < p2.id
    RETURN p1.id AS source,
           coalesce(substring(p1.caption, 0, 80), p1.id) AS source_label,
           p2.id AS target,
           coalesce(substring(p2.caption, 0, 80), p2.id) AS target_label,
           count(DISTINCT u) AS weight
    ORDER BY weight DESC
    LIMIT $limit
    """

    with get_neo4j_session() as session:
        records = session.run(query, limit=limit).data()

    nodes = {}
    edges = []

    for row in records:
        nodes[row["source"]] = {
            "id": row["source"],
            "label": row["source_label"],
            "type": "post",
            "group": "InstagramPost"
        }

        nodes[row["target"]] = {
            "id": row["target"],
            "label": row["target_label"],
            "type": "post",
            "group": "InstagramPost"
        }

        edges.append({
            "source": row["source"],
            "target": row["target"],
            "weight": row["weight"],
            "type": "IG_POST_TO_POST"
        })

    return build_response("instagram", 3, nodes, edges)