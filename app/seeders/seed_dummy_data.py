import random
from datetime import datetime, timedelta
from app.database import get_neo4j_session


# ============================================================
# CONFIG JUMLAH DATA - VERSI AURA AMAN
# ============================================================

USER_COUNT = 25000

KAWANSS_POST_COUNT = 2500
INFOSS_POST_COUNT = 1500

KAWANSS_COMMENT_COUNT = 8000
INFOSS_COMMENT_COUNT = 6000

FIREBASE_LIKE_COUNT = 30000

INSTAGRAM_USER_COUNT = 10000
INSTAGRAM_POST_COUNT = 1500
INSTAGRAM_COMMENT_COUNT = 8000
INSTAGRAM_LIKE_COUNT = 25000

BATCH_SIZE = 1000


HASHTAGS = [
    "surabaya",
    "suarasurabaya",
    "traffic",
    "kecelakaan",
    "cuaca",
    "banjir",
    "jalanraya",
    "event",
    "pendidikan",
    "kesehatan",
    "kuliner",
    "info",
    "warganet",
    "radio",
    "berita",
    "otomotif",
    "komunitas",
    "laporanwarga",
    "kriminal",
    "ekonomi",
    "politik",
    "transportasi",
    "macet",
    "viral",
    "jatim",
    "gresik",
    "sidoarjo",
    "malang",
    "mojokerto",
    "pasuruan"
]


# ============================================================
# UTIL
# ============================================================

def random_date(days_back=180):
    value = datetime.now() - timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    return value.isoformat()


def random_city():
    return random.choice([
        "Surabaya",
        "Sidoarjo",
        "Gresik",
        "Malang",
        "Mojokerto",
        "Pasuruan",
        "Lamongan",
        "Jombang",
        "Kediri",
        "Bangkalan"
    ])


def print_progress(name, current, total):
    print(f"{name}: {current}/{total}")


# ============================================================
# CLEAR ALL DATA
# ============================================================

def clear_all_data(session):
    print("Clearing all existing data...")

    query = """
    MATCH (n)
    DETACH DELETE n
    """

    session.run(query)
    print("All existing data cleared.")


# ============================================================
# SHARED: HASHTAG
# ============================================================

def seed_hashtags(session):
    print("Seeding hashtags...")

    data = [{"name": tag} for tag in HASHTAGS]

    query = """
    UNWIND $hashtags AS hashtag
    MERGE (h:Hashtag {name: hashtag.name})
    SET h.createdAt = datetime()
    """

    session.run(query, {"hashtags": data})
    print("Hashtags seeded.")


# ============================================================
# INSTAGRAM PROFILE
# ============================================================

def seed_insta_profile(session):
    print("Seeding InstaProfile and official InstagramUser...")

    query = """
    MERGE (profile:InstaProfile {id: $id})
    SET profile.username = $username,
        profile.name = $name,
        profile.biography = $biography,
        profile.followers_count = $followers_count,
        profile.follows_count = $follows_count,
        profile.media_count = $media_count,
        profile.profile_picture_url = $profile_picture_url,
        profile.createdAt = datetime()

    MERGE (u:InstagramUser {username: $username})
    SET u.full_name = $name,
        u.profile_picture_url = $profile_picture_url,
        u.followers_count = $followers_count,
        u.follows_count = $follows_count,
        u.media_count = $media_count,
        u.is_private = false,
        u.is_verified = true,
        u.is_official_profile = true,
        u.createdAt = datetime()

    MERGE (profile)-[:OWNS_IG_ACCOUNT]->(u)
    """

    session.run(query, {
        "id": "17841402333785817",
        "username": "suarasurabayamedia",
        "name": "SUARA SURABAYA",
        "biography": (
            "Official Instagram Radio Suara Surabaya\n"
            "Official Organizer @jazztraffic @suarasurabayaacademy @soerabaja10k\n"
            "Multifunction Hall @suarasurabaya.centre"
        ),
        "followers_count": 925319,
        "follows_count": 37,
        "media_count": 44869,
        "profile_picture_url": (
            "https://scontent-sof1-1.xx.fbcdn.net/v/t51.82787-15/"
            "657742100_18521535727077793_8249595370017850007_n.jpg"
        )
    })

    print("InstaProfile and official InstagramUser seeded.")


# ============================================================
# FIREBASE USER
# ============================================================

def seed_firebase_users(session):
    print(f"Seeding {USER_COUNT} FirebaseUser nodes...")

    roles = ["user", "kawanss", "member"]

    for start in range(1, USER_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, USER_COUNT + 1)

        for i in range(start, end):
            created_at = random_date()

            batch.append({
                "id": f"dummy_user_{i}",
                "nama": f"User Dummy {i}",
                "username": f"userdummy{i}",
                "email": f"userdummy{i}@example.com",
                "old_mysql_id": i,
                "role": random.choice(roles),
                "old_status_code": 1,
                "old_token": str(random.randint(100000, 999999)),
                "alamat": random_city(),
                "aktivitas": "Aktif menggunakan aplikasi UAT",
                "photoURL": "",
                "createdAt": created_at,
                "joinDate": created_at,
                "old_id_int": i,
                "isDeleted": False,
                "jumlahShare": random.randint(0, 100),
                "hakAkses": "user",
                "jumlahKontributor": random.randint(0, 20),
                "old_updated_at": created_at,
                "nomorHp": f"0812{str(i).zfill(8)}",
                "jumlahLike": random.randint(0, 500),
                "jumlahComment": random.randint(0, 300),
                "jenis_kelamin": random.choice(["L", "P"]),
                "verificationToken": "",
                "nomor_hp": f"0812{str(i).zfill(8)}",
                "jenisKelamin": random.choice(["Laki-laki", "Perempuan"]),
                "photoUrl": "",
                "status": "active",
                "roleId": "role_user",
                "poin": random.randint(0, 1000),
                "photoProfileURL": "",
                "callable": True,
                "updatedAt": created_at,
                "tanggal_lahir": "1998-01-01",
                "poinHistory": "[]",
                "isVerified": True,
                "jumlahPostKawanSS": random.randint(0, 10),
                "ban": False,
                "phone": f"0812{str(i).zfill(8)}",
                "tanggalLahir": "1998-01-01"
            })

        query = """
        UNWIND $users AS user
        MERGE (u:FirebaseUser {id: user.id})
        SET u.nama = user.nama,
            u.username = user.username,
            u.email = user.email,
            u.old_mysql_id = user.old_mysql_id,
            u.role = user.role,
            u.old_status_code = user.old_status_code,
            u.old_token = user.old_token,
            u.alamat = user.alamat,
            u.aktivitas = user.aktivitas,
            u.photoURL = user.photoURL,
            u.createdAt = user.createdAt,
            u.joinDate = user.joinDate,
            u.old_id_int = user.old_id_int,
            u.isDeleted = user.isDeleted,
            u.jumlahShare = user.jumlahShare,
            u.hakAkses = user.hakAkses,
            u.jumlahKontributor = user.jumlahKontributor,
            u.old_updated_at = user.old_updated_at,
            u.nomorHp = user.nomorHp,
            u.jumlahLike = user.jumlahLike,
            u.jumlahComment = user.jumlahComment,
            u.jenis_kelamin = user.jenis_kelamin,
            u.verificationToken = user.verificationToken,
            u.nomor_hp = user.nomor_hp,
            u.jenisKelamin = user.jenisKelamin,
            u.photoUrl = user.photoUrl,
            u.status = user.status,
            u.roleId = user.roleId,
            u.poin = user.poin,
            u.photoProfileURL = user.photoProfileURL,
            u.callable = user.callable,
            u.updatedAt = user.updatedAt,
            u.tanggal_lahir = user.tanggal_lahir,
            u.poinHistory = user.poinHistory,
            u.isVerified = user.isVerified,
            u.jumlahPostKawanSS = user.jumlahPostKawanSS,
            u.ban = user.ban,
            u.phone = user.phone,
            u.tanggalLahir = user.tanggalLahir
        """

        session.run(query, {"users": batch})
        print_progress("FirebaseUser", end - 1, USER_COUNT)

    print("FirebaseUser seeded.")


# ============================================================
# FIREBASE KAWANSS POST
# ============================================================

def seed_firebase_kawanss_posts(session):
    print(f"Seeding {KAWANSS_POST_COUNT} FirebaseKawanSS posts...")

    for start in range(1, KAWANSS_POST_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, KAWANSS_POST_COUNT + 1)

        for i in range(start, end):
            user_id = f"dummy_user_{random.randint(1, USER_COUNT)}"
            created_at = random_date()
            hashtag_sample = random.sample(HASHTAGS, random.randint(1, 4))
            hashtag_text = " ".join([f"#{tag}" for tag in hashtag_sample])

            batch.append({
                "id": f"dummy_kawanss_{i}",
                "judul": f"Laporan KawanSS Dummy {i}",
                "title": f"Laporan KawanSS Dummy {i}",
                "deskripsi": f"Ini adalah laporan dummy KawanSS nomor {i}. {hashtag_text}",
                "old_mysql_id": str(i),
                "photoURL": "",
                "createdAt": created_at,
                "joinDate": created_at,
                "old_id_int": i,
                "isDeleted": False,
                "jumlahShare": random.randint(0, 200),
                "jumlahLike": random.randint(0, 1000),
                "jumlahComment": random.randint(0, 300),
                "jumlahView": random.randint(100, 50000),
                "accountName": f"User Dummy {user_id.split('_')[-1]}",
                "old_kontributor_id": str(random.randint(1, USER_COUNT)),
                "lokasi": random_city(),
                "deleted": False,
                "gambar": "",
                "titlee": f"Laporan KawanSS Dummy {i}",
                "collectionName": "kawanss",
                "detail": f"Detail laporan dummy KawanSS nomor {i}.",
                "updatedAt": created_at,
                "jumlahLaporan": random.randint(0, 20),
                "kawanssPhotoURL": "",
                "kontributorPhotoURL": "",
                "userId": user_id,
                "deletedAt": "",
                "uploadDate": created_at,
                "old_counter": random.randint(0, 1000),
                "hashtags": hashtag_sample
            })

        query = """
        UNWIND $posts AS post
        MATCH (u:FirebaseUser {id: post.userId})
        MERGE (p:FirebaseKawanSS {id: post.id})
        SET p.judul = post.judul,
            p.title = post.title,
            p.deskripsi = post.deskripsi,
            p.old_mysql_id = post.old_mysql_id,
            p.photoURL = post.photoURL,
            p.createdAt = post.createdAt,
            p.joinDate = post.joinDate,
            p.old_id_int = post.old_id_int,
            p.isDeleted = post.isDeleted,
            p.jumlahShare = post.jumlahShare,
            p.jumlahLike = post.jumlahLike,
            p.jumlahComment = post.jumlahComment,
            p.jumlahView = post.jumlahView,
            p.accountName = post.accountName,
            p.old_kontributor_id = post.old_kontributor_id,
            p.lokasi = post.lokasi,
            p.deleted = post.deleted,
            p.gambar = post.gambar,
            p.titlee = post.titlee,
            p.collectionName = post.collectionName,
            p.detail = post.detail,
            p.updatedAt = post.updatedAt,
            p.jumlahLaporan = post.jumlahLaporan,
            p.kawanssPhotoURL = post.kawanssPhotoURL,
            p.kontributorPhotoURL = post.kontributorPhotoURL,
            p.userId = post.userId,
            p.deletedAt = post.deletedAt,
            p.uploadDate = post.uploadDate,
            p.old_counter = post.old_counter
        MERGE (u)-[:POSTED_FB]->(p)
        WITH p, post
        UNWIND post.hashtags AS tag
        MATCH (h:Hashtag {name: tag})
        MERGE (p)-[:HAS_HASHTAG]->(h)
        """

        session.run(query, {"posts": batch})
        print_progress("FirebaseKawanSS", end - 1, KAWANSS_POST_COUNT)

    print("FirebaseKawanSS seeded.")


# ============================================================
# FIREBASE INFOSS POST
# ============================================================

def seed_firebase_infoss_posts(session):
    print(f"Seeding {INFOSS_POST_COUNT} FirebaseInfoss posts...")

    for start in range(1, INFOSS_POST_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, INFOSS_POST_COUNT + 1)

        for i in range(start, end):
            user_id = f"dummy_user_{random.randint(1, USER_COUNT)}"
            created_at = random_date()
            hashtag_sample = random.sample(HASHTAGS, random.randint(1, 4))
            hashtag_text = " ".join([f"#{tag}" for tag in hashtag_sample])

            batch.append({
                "id": f"dummy_infoss_{i}",
                "judul": f"Berita Infoss Dummy {i}",
                "title": f"Berita Infoss Dummy {i}",
                "deskripsi": f"Ini adalah berita dummy Infoss nomor {i}. {hashtag_text}",
                "createdAt": created_at,
                "isDeleted": False,
                "jumlahShare": random.randint(0, 300),
                "jumlahLike": random.randint(0, 2000),
                "jumlahComment": random.randint(0, 500),
                "jumlahView": random.randint(1000, 100000),
                "uploadDate": created_at,
                "updatedAt": created_at,
                "userId": user_id,
                "hashtags": hashtag_sample
            })

        query = """
        UNWIND $posts AS post
        MATCH (u:FirebaseUser {id: post.userId})
        MERGE (p:FirebaseInfoss {id: post.id})
        SET p.judul = post.judul,
            p.title = post.title,
            p.deskripsi = post.deskripsi,
            p.createdAt = post.createdAt,
            p.isDeleted = post.isDeleted,
            p.jumlahShare = post.jumlahShare,
            p.jumlahLike = post.jumlahLike,
            p.jumlahComment = post.jumlahComment,
            p.jumlahView = post.jumlahView,
            p.uploadDate = post.uploadDate,
            p.updatedAt = post.updatedAt,
            p.userId = post.userId
        MERGE (u)-[:POSTED_FB]->(p)
        WITH p, post
        UNWIND post.hashtags AS tag
        MATCH (h:Hashtag {name: tag})
        MERGE (p)-[:HAS_HASHTAG]->(h)
        """

        session.run(query, {"posts": batch})
        print_progress("FirebaseInfoss", end - 1, INFOSS_POST_COUNT)

    print("FirebaseInfoss seeded.")


# ============================================================
# FIREBASE KAWANSS COMMENT + REPLY
# ============================================================

def seed_firebase_kawanss_comments(session):
    print(f"Seeding {KAWANSS_COMMENT_COUNT} FirebaseKawanSSComment nodes...")

    for start in range(1, KAWANSS_COMMENT_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, KAWANSS_COMMENT_COUNT + 1)

        for i in range(start, end):
            user_number = random.randint(1, USER_COUNT)
            user_id = f"dummy_user_{user_number}"
            post_id = f"dummy_kawanss_{random.randint(1, KAWANSS_POST_COUNT)}"
            created_at = random_date()

            is_reply = i > 100 and random.random() < 0.35
            reply_to_id = f"dummy_kawanss_comment_{random.randint(1, i - 1)}" if is_reply else ""

            batch.append({
                "id": f"dummy_kawanss_comment_{i}",
                "username": f"userdummy{user_number}",
                "old_mysql_id": str(i),
                "photoURL": "",
                "createdAt": created_at,
                "isDeleted": False,
                "jumlahLike": random.randint(0, 200),
                "accountName": f"User Dummy {user_number}",
                "jumlahDislike": random.randint(0, 20),
                "likedUsers": "[]",
                "comment": f"Komentar dummy KawanSS nomor {i}",
                "replyToId": reply_to_id,
                "kawanssId": post_id,
                "infossUid": "",
                "old_newsid": "",
                "kawanssUid": post_id,
                "userUid": user_id,
                "deleted": False,
                "rootId": reply_to_id if is_reply else "",
                "updatedAt": created_at,
                "userId": user_id,
                "isReply": is_reply,
                "deletedAt": "",
                "old_jenis": "kawanss",
                "uploadDate": created_at,
                "userPhotoProfileURL": "",
                "jumlahReplies": random.randint(0, 10),
                "dislikedUsers": "[]"
            })

        query = """
        UNWIND $comments AS comment
        MATCH (u:FirebaseUser {id: comment.userId})
        MATCH (p:FirebaseKawanSS {id: comment.kawanssId})
        MERGE (c:FirebaseKawanSSComment {id: comment.id})
        SET c.username = comment.username,
            c.old_mysql_id = comment.old_mysql_id,
            c.photoURL = comment.photoURL,
            c.createdAt = comment.createdAt,
            c.isDeleted = comment.isDeleted,
            c.jumlahLike = comment.jumlahLike,
            c.accountName = comment.accountName,
            c.jumlahDislike = comment.jumlahDislike,
            c.likedUsers = comment.likedUsers,
            c.comment = comment.comment,
            c.replyToId = comment.replyToId,
            c.kawanssId = comment.kawanssId,
            c.infossUid = comment.infossUid,
            c.old_newsid = comment.old_newsid,
            c.kawanssUid = comment.kawanssUid,
            c.userUid = comment.userUid,
            c.deleted = comment.deleted,
            c.rootId = comment.rootId,
            c.updatedAt = comment.updatedAt,
            c.userId = comment.userId,
            c.isReply = comment.isReply,
            c.deletedAt = comment.deletedAt,
            c.old_jenis = comment.old_jenis,
            c.uploadDate = comment.uploadDate,
            c.userPhotoProfileURL = comment.userPhotoProfileURL,
            c.jumlahReplies = comment.jumlahReplies,
            c.dislikedUsers = comment.dislikedUsers
        MERGE (u)-[:WROTE_FB]->(c)
        MERGE (c)-[:COMMENTED_ON_FB]->(p)
        WITH c, comment
        OPTIONAL MATCH (parent:FirebaseKawanSSComment {id: comment.replyToId})
        FOREACH (_ IN CASE WHEN parent IS NULL THEN [] ELSE [1] END |
            MERGE (c)-[:REPLIED_TO_FB]->(parent)
        )
        """

        session.run(query, {"comments": batch})
        print_progress("FirebaseKawanSSComment", end - 1, KAWANSS_COMMENT_COUNT)

    print("FirebaseKawanSSComment seeded.")


# ============================================================
# FIREBASE INFOSS COMMENT + REPLY
# ============================================================

def seed_firebase_infoss_comments(session):
    print(f"Seeding {INFOSS_COMMENT_COUNT} FirebaseInfossComment nodes...")

    for start in range(1, INFOSS_COMMENT_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, INFOSS_COMMENT_COUNT + 1)

        for i in range(start, end):
            user_number = random.randint(1, USER_COUNT)
            user_id = f"dummy_user_{user_number}"
            post_id = f"dummy_infoss_{random.randint(1, INFOSS_POST_COUNT)}"
            created_at = random_date()

            is_reply = i > 100 and random.random() < 0.35
            reply_to_id = f"dummy_infoss_comment_{random.randint(1, i - 1)}" if is_reply else ""

            batch.append({
                "id": f"dummy_infoss_comment_{i}",
                "username": f"userdummy{user_number}",
                "old_mysql_id": str(i),
                "photoURL": "",
                "createdAt": created_at,
                "isDeleted": False,
                "jumlahLike": random.randint(0, 200),
                "accountName": f"User Dummy {user_number}",
                "jumlahDislike": random.randint(0, 20),
                "likedUsers": "[]",
                "comment": f"Komentar dummy Infoss nomor {i}",
                "replyToId": reply_to_id,
                "infossUid": post_id,
                "kawanssUid": "",
                "old_newsid": "",
                "userUid": user_id,
                "deleted": False,
                "infossId": post_id,
                "rootId": reply_to_id if is_reply else "",
                "updatedAt": created_at,
                "userId": user_id,
                "isReply": is_reply,
                "old_jenis": "infoss",
                "uploadDate": created_at,
                "userPhotoProfileURL": "",
                "jumlahReplies": random.randint(0, 10),
                "dislikedUsers": "[]"
            })

        query = """
        UNWIND $comments AS comment
        MATCH (u:FirebaseUser {id: comment.userId})
        MATCH (p:FirebaseInfoss {id: comment.infossId})
        MERGE (c:FirebaseInfossComment {id: comment.id})
        SET c.username = comment.username,
            c.old_mysql_id = comment.old_mysql_id,
            c.photoURL = comment.photoURL,
            c.createdAt = comment.createdAt,
            c.isDeleted = comment.isDeleted,
            c.jumlahLike = comment.jumlahLike,
            c.accountName = comment.accountName,
            c.jumlahDislike = comment.jumlahDislike,
            c.likedUsers = comment.likedUsers,
            c.comment = comment.comment,
            c.replyToId = comment.replyToId,
            c.infossUid = comment.infossUid,
            c.kawanssUid = comment.kawanssUid,
            c.old_newsid = comment.old_newsid,
            c.userUid = comment.userUid,
            c.deleted = comment.deleted,
            c.infossId = comment.infossId,
            c.rootId = comment.rootId,
            c.updatedAt = comment.updatedAt,
            c.userId = comment.userId,
            c.isReply = comment.isReply,
            c.old_jenis = comment.old_jenis,
            c.uploadDate = comment.uploadDate,
            c.userPhotoProfileURL = comment.userPhotoProfileURL,
            c.jumlahReplies = comment.jumlahReplies,
            c.dislikedUsers = comment.dislikedUsers
        MERGE (u)-[:WROTE_FB]->(c)
        MERGE (c)-[:COMMENTED_ON_FB]->(p)
        WITH c, comment
        OPTIONAL MATCH (parent:FirebaseInfossComment {id: comment.replyToId})
        FOREACH (_ IN CASE WHEN parent IS NULL THEN [] ELSE [1] END |
            MERGE (c)-[:REPLIED_TO_FB]->(parent)
        )
        """

        session.run(query, {"comments": batch})
        print_progress("FirebaseInfossComment", end - 1, INFOSS_COMMENT_COUNT)

    print("FirebaseInfossComment seeded.")


# ============================================================
# FIREBASE LIKE
# ============================================================

def seed_firebase_likes(session):
    print(f"Seeding {FIREBASE_LIKE_COUNT} FirebaseLike nodes...")

    for start in range(1, FIREBASE_LIKE_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, FIREBASE_LIKE_COUNT + 1)

        for i in range(start, end):
            user_id = f"dummy_user_{random.randint(1, USER_COUNT)}"

            if random.random() < 0.6:
                target_id = f"dummy_kawanss_{random.randint(1, KAWANSS_POST_COUNT)}"
                target_type = "kawanss"
            else:
                target_id = f"dummy_infoss_{random.randint(1, INFOSS_POST_COUNT)}"
                target_type = "infoss"

            batch.append({
                "id": f"dummy_like_{i}",
                "userId": user_id,
                "targetId": target_id,
                "targetType": target_type,
                "createdAt": random_date()
            })

        query = """
        UNWIND $likes AS like
        MATCH (u:FirebaseUser {id: like.userId})
        MERGE (l:FirebaseLike {id: like.id})
        SET l.userId = like.userId,
            l.targetId = like.targetId,
            l.targetType = like.targetType,
            l.createdAt = like.createdAt
        MERGE (u)-[:LIKED_FB]->(l)
        WITH l, like
        OPTIONAL MATCH (k:FirebaseKawanSS {id: like.targetId})
        OPTIONAL MATCH (i:FirebaseInfoss {id: like.targetId})
        FOREACH (_ IN CASE WHEN k IS NULL THEN [] ELSE [1] END |
            MERGE (l)-[:LIKED_TARGET_FB]->(k)
        )
        FOREACH (_ IN CASE WHEN i IS NULL THEN [] ELSE [1] END |
            MERGE (l)-[:LIKED_TARGET_FB]->(i)
        )
        """

        session.run(query, {"likes": batch})
        print_progress("FirebaseLike", end - 1, FIREBASE_LIKE_COUNT)

    print("FirebaseLike seeded.")


# ============================================================
# INSTAGRAM USER
# ============================================================

def seed_instagram_users(session):
    print(f"Seeding {INSTAGRAM_USER_COUNT} InstagramUser nodes...")

    for start in range(1, INSTAGRAM_USER_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, INSTAGRAM_USER_COUNT + 1)

        for i in range(start, end):
            batch.append({
                "username": f"ig_user_dummy_{i}",
                "full_name": f"Instagram User Dummy {i}",
                "profile_picture_url": "",
                "followers_count": random.randint(10, 50000),
                "follows_count": random.randint(10, 3000),
                "media_count": random.randint(0, 1000),
                "is_private": random.choice([False, False, False, True]),
                "is_verified": random.choice([False, False, False, True]),
                "createdAt": random_date()
            })

        query = """
        UNWIND $users AS user
        MERGE (u:InstagramUser {username: user.username})
        SET u.full_name = user.full_name,
            u.profile_picture_url = user.profile_picture_url,
            u.followers_count = user.followers_count,
            u.follows_count = user.follows_count,
            u.media_count = user.media_count,
            u.is_private = user.is_private,
            u.is_verified = user.is_verified,
            u.createdAt = user.createdAt
        """

        session.run(query, {"users": batch})
        print_progress("InstagramUser", end - 1, INSTAGRAM_USER_COUNT)

    print("InstagramUser seeded.")


# ============================================================
# INSTAGRAM POST
# ============================================================

def seed_instagram_posts(session):
    print(f"Seeding {INSTAGRAM_POST_COUNT} InstagramPost nodes...")

    media_types = ["IMAGE", "VIDEO", "CAROUSEL_ALBUM"]

    for start in range(1, INSTAGRAM_POST_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, INSTAGRAM_POST_COUNT + 1)

        for i in range(start, end):
            timestamp = random_date()
            hashtag_sample = random.sample(HASHTAGS, random.randint(1, 5))
            hashtag_text = " ".join([f"#{tag}" for tag in hashtag_sample])

            batch.append({
                "id": f"dummy_ig_post_{i}",
                "timestamp": timestamp,
                "comments_count": random.randint(0, 2000),
                "permalink": f"https://instagram.com/p/dummy_ig_post_{i}",
                "view_count": random.randint(1000, 500000),
                "like_count": random.randint(100, 100000),
                "caption": f"Dummy Instagram post Suara Surabaya nomor {i}. {hashtag_text}",
                "share_count": random.randint(0, 10000),
                "media_type": random.choice(media_types),
                "hashtags": hashtag_sample,
                "owner_username": "suarasurabayamedia"
            })

        query = """
        UNWIND $posts AS post
        MATCH (owner:InstagramUser {username: post.owner_username})
        MERGE (p:InstagramPost {id: post.id})
        SET p.timestamp = post.timestamp,
            p.comments_count = post.comments_count,
            p.permalink = post.permalink,
            p.view_count = post.view_count,
            p.like_count = post.like_count,
            p.caption = post.caption,
            p.share_count = post.share_count,
            p.media_type = post.media_type
        MERGE (owner)-[:POSTED_IG]->(p)
        WITH p, post
        UNWIND post.hashtags AS tag
        MATCH (h:Hashtag {name: tag})
        MERGE (p)-[:HAS_HASHTAG]->(h)
        """

        session.run(query, {"posts": batch})
        print_progress("InstagramPost", end - 1, INSTAGRAM_POST_COUNT)

    print("InstagramPost seeded.")


# ============================================================
# INSTAGRAM COMMENT + REPLY
# ============================================================

def seed_instagram_comments(session):
    print(f"Seeding {INSTAGRAM_COMMENT_COUNT} InstagramComment nodes...")

    for start in range(1, INSTAGRAM_COMMENT_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, INSTAGRAM_COMMENT_COUNT + 1)

        for i in range(start, end):
            username = f"ig_user_dummy_{random.randint(1, INSTAGRAM_USER_COUNT)}"
            post_id = f"dummy_ig_post_{random.randint(1, INSTAGRAM_POST_COUNT)}"
            is_reply = i > 100 and random.random() < 0.35
            reply_to_id = f"dummy_ig_comment_{random.randint(1, i - 1)}" if is_reply else ""

            batch.append({
                "id": f"dummy_ig_comment_{i}",
                "timestamp": random_date(),
                "likes": random.randint(0, 500),
                "type": "reply" if is_reply else "comment",
                "replies_count": random.randint(0, 20),
                "text": f"Komentar dummy Instagram nomor {i}",
                "username": username,
                "post_id": post_id,
                "reply_to_id": reply_to_id
            })

        query = """
        UNWIND $comments AS comment
        MATCH (u:InstagramUser {username: comment.username})
        MATCH (p:InstagramPost {id: comment.post_id})
        MERGE (c:InstagramComment {id: comment.id})
        SET c.timestamp = comment.timestamp,
            c.likes = comment.likes,
            c.type = comment.type,
            c.replies_count = comment.replies_count,
            c.text = comment.text,
            c.username = comment.username,
            c.post_id = comment.post_id,
            c.reply_to_id = comment.reply_to_id
        MERGE (u)-[:WROTE_IG]->(c)
        MERGE (c)-[:COMMENTED_ON_IG]->(p)
        WITH c, comment
        OPTIONAL MATCH (parent:InstagramComment {id: comment.reply_to_id})
        FOREACH (_ IN CASE WHEN parent IS NULL THEN [] ELSE [1] END |
            MERGE (c)-[:REPLIED_TO_IG]->(parent)
        )
        """

        session.run(query, {"comments": batch})
        print_progress("InstagramComment", end - 1, INSTAGRAM_COMMENT_COUNT)

    print("InstagramComment seeded.")


# ============================================================
# INSTAGRAM LIKE
# ============================================================

def seed_instagram_likes(session):
    print(f"Seeding {INSTAGRAM_LIKE_COUNT} InstagramLike nodes...")

    for start in range(1, INSTAGRAM_LIKE_COUNT + 1, BATCH_SIZE):
        batch = []
        end = min(start + BATCH_SIZE, INSTAGRAM_LIKE_COUNT + 1)

        for i in range(start, end):
            batch.append({
                "id": f"dummy_ig_like_{i}",
                "username": f"ig_user_dummy_{random.randint(1, INSTAGRAM_USER_COUNT)}",
                "post_id": f"dummy_ig_post_{random.randint(1, INSTAGRAM_POST_COUNT)}",
                "createdAt": random_date()
            })

        query = """
        UNWIND $likes AS like
        MATCH (u:InstagramUser {username: like.username})
        MATCH (p:InstagramPost {id: like.post_id})
        MERGE (l:InstagramLike {id: like.id})
        SET l.username = like.username,
            l.post_id = like.post_id,
            l.createdAt = like.createdAt
        MERGE (u)-[:LIKED_IG]->(l)
        MERGE (l)-[:LIKED_TARGET_IG]->(p)
        """

        session.run(query, {"likes": batch})
        print_progress("InstagramLike", end - 1, INSTAGRAM_LIKE_COUNT)

    print("InstagramLike seeded.")


# ============================================================
# MAIN SEEDER
# ============================================================

def run_seeder(clear_existing=True):
    with get_neo4j_session() as session:
        if clear_existing:
            clear_all_data(session)

        seed_hashtags(session)

        seed_insta_profile(session)

        seed_firebase_users(session)
        seed_firebase_kawanss_posts(session)
        seed_firebase_infoss_posts(session)
        seed_firebase_kawanss_comments(session)
        seed_firebase_infoss_comments(session)
        seed_firebase_likes(session)

        seed_instagram_users(session)
        seed_instagram_posts(session)
        seed_instagram_comments(session)
        seed_instagram_likes(session)

    print("All UAT data seeded successfully.")