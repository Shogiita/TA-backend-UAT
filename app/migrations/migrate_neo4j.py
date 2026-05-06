from app.database import get_neo4j_session


def run_migration():
    queries = [
        # =========================
        # FIREBASE / APP CONSTRAINTS
        # =========================
        """
        CREATE CONSTRAINT firebase_user_id_unique IF NOT EXISTS
        FOR (u:FirebaseUser)
        REQUIRE u.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT firebase_kawanss_id_unique IF NOT EXISTS
        FOR (p:FirebaseKawanSS)
        REQUIRE p.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT firebase_infoss_id_unique IF NOT EXISTS
        FOR (p:FirebaseInfoss)
        REQUIRE p.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT firebase_kawanss_comment_id_unique IF NOT EXISTS
        FOR (c:FirebaseKawanSSComment)
        REQUIRE c.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT firebase_infoss_comment_id_unique IF NOT EXISTS
        FOR (c:FirebaseInfossComment)
        REQUIRE c.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT firebase_like_id_unique IF NOT EXISTS
        FOR (l:FirebaseLike)
        REQUIRE l.id IS UNIQUE
        """,

        # =========================
        # INSTAGRAM CONSTRAINTS
        # =========================
        """
        CREATE CONSTRAINT insta_profile_id_unique IF NOT EXISTS
        FOR (p:InstaProfile)
        REQUIRE p.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT instagram_user_username_unique IF NOT EXISTS
        FOR (u:InstagramUser)
        REQUIRE u.username IS UNIQUE
        """,
        """
        CREATE CONSTRAINT instagram_post_id_unique IF NOT EXISTS
        FOR (p:InstagramPost)
        REQUIRE p.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT instagram_comment_id_unique IF NOT EXISTS
        FOR (c:InstagramComment)
        REQUIRE c.id IS UNIQUE
        """,
        """
        CREATE CONSTRAINT instagram_like_id_unique IF NOT EXISTS
        FOR (l:InstagramLike)
        REQUIRE l.id IS UNIQUE
        """,

        # =========================
        # SHARED CONSTRAINTS
        # =========================
        """
        CREATE CONSTRAINT hashtag_name_unique IF NOT EXISTS
        FOR (h:Hashtag)
        REQUIRE h.name IS UNIQUE
        """,

        # =========================
        # FIREBASE / APP INDEXES
        # =========================
        """
        CREATE INDEX firebase_user_created_at_index IF NOT EXISTS
        FOR (u:FirebaseUser)
        ON (u.createdAt)
        """,
        """
        CREATE INDEX firebase_user_username_index IF NOT EXISTS
        FOR (u:FirebaseUser)
        ON (u.username)
        """,
        """
        CREATE INDEX firebase_kawanss_created_at_index IF NOT EXISTS
        FOR (p:FirebaseKawanSS)
        ON (p.createdAt)
        """,
        """
        CREATE INDEX firebase_infoss_created_at_index IF NOT EXISTS
        FOR (p:FirebaseInfoss)
        ON (p.createdAt)
        """,
        """
        CREATE INDEX kawanss_comment_created_at_index IF NOT EXISTS
        FOR (c:FirebaseKawanSSComment)
        ON (c.createdAt)
        """,
        """
        CREATE INDEX infoss_comment_created_at_index IF NOT EXISTS
        FOR (c:FirebaseInfossComment)
        ON (c.createdAt)
        """,
        """
        CREATE INDEX firebase_like_created_at_index IF NOT EXISTS
        FOR (l:FirebaseLike)
        ON (l.createdAt)
        """,

        # =========================
        # INSTAGRAM INDEXES
        # =========================
        """
        CREATE INDEX instagram_post_timestamp_index IF NOT EXISTS
        FOR (p:InstagramPost)
        ON (p.timestamp)
        """,
        """
        CREATE INDEX instagram_comment_timestamp_index IF NOT EXISTS
        FOR (c:InstagramComment)
        ON (c.timestamp)
        """,
        """
        CREATE INDEX instagram_user_username_index IF NOT EXISTS
        FOR (u:InstagramUser)
        ON (u.username)
        """,
        """
        CREATE INDEX instagram_like_created_at_index IF NOT EXISTS
        FOR (l:InstagramLike)
        ON (l.createdAt)
        """
    ]

    with get_neo4j_session() as session:
        for query in queries:
            session.run(query)

    print("Migration completed successfully.")