import mysql.connector
from mysql.connector import connect, Error
from datetime import datetime


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="movie_tracker"
        )
        return conn
    except Exception as e:
        print("Failed to connect to DB:", e)
        return None



def create_user(full_name, age, gender, email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (full_name, age, gender, email, password) VALUES (%s, %s, %s, %s, %s)",
                       (full_name, age, gender, email, password))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Database error:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def validate_login(email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # ← return dicts
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as e:
        print("Login error:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def add_to_watch(user_id, title):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO to_watch (user_id, title) VALUES (%s, %s)", (user_id, title))
        conn.commit()
        return True
    except Error as e:
        print("Error adding movie:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def get_to_watch(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM to_watch WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    except Error as e:
        print("Error fetching list:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def remove_to_watch(movie_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM to_watch WHERE id = %s", (movie_id,))
        conn.commit()
        return True
    except Error as e:
        print("Error deleting movie:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def add_watched_movie(user_id, title, rating, review):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO watched (user_id, title, rating, review)
            VALUES (%s, %s, %s, %s)
        """, (user_id, title, rating, review))
        conn.commit()
        return True
    except Error as e:
        print("Error adding watched movie:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def add_to_watchlist(user_id, movie):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO watchlist (user_id, movie_id, title, poster_path, release_year) VALUES (%s, %s, %s, %s, %s)"
        values = (
            user_id,
            movie.get("id"),
            movie.get("title"),
            movie.get("poster_path"),
            movie.get("release_date", "")[:4]
        )
        cursor.execute(sql, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Error saving to watchlist:", err)
        return False


def get_watchlist(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, poster_path, release_year
            FROM watchlist
            WHERE user_id = %s 
        """, (user_id,))
        return cursor.fetchall()
    except Error as e:
        print("Error fetching watchlist:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def remove_to_watch(movie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM watchlist WHERE id = %s", (movie_id,))
    conn.commit()
    conn.close()



################################
def add_to_watched(user_id, movie, rating=None, review=None):
    try:
        db = get_connection()
        cursor = db.cursor()

        query = """
            INSERT INTO watched (user_id, movie_id, title, release_year, poster_path, review, rating, watched_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        date_now = datetime.now().strftime('%Y-%m-%d')  # ← Add this
        values = (
            user_id,
            movie.get("id"),
            movie.get("title"),
            movie.get("release_date", "")[:4],
            movie.get("poster_path"),
            review,
            int(rating),
            date_now
        )

        cursor.execute(query, values)
        db.commit()
        return True
    except mysql.connector.Error as err:
        print("Error saving watched movie:", err)
        return False



def get_watched_movies(user_id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM watched WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error loading watched list:", err)
        return []


#################################

def move_to_watched(user_id, movie_id, movie, review="", rating=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO watched (user_id, movie_id, title, release_year, poster_path, review, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            movie_id,
            movie.get("title", ""),
            movie.get("release_date", "")[:4],
            movie.get("poster_path", ""),
            review,
            int(rating),
        )
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as err:
        print("Error adding to watched list:", err)



def get_watched(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM watched WHERE user_id = %s ORDER BY id DESC", (user_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error fetching watched list:", err)
        return []




def remove_from_watched(movie_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watched WHERE id = %s", (movie_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error deleting from watched:", err)


def update_review_rating(movie_id, review, rating):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE watched SET review = %s, rating = %s WHERE id = %s",
                       (review, rating, movie_id))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error updating review and rating:", err)


def get_watched_count(user_id: int) -> int:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM watched WHERE user_id=%s", (user_id,))
        return cur.fetchone()[0]
    except Exception as e:
        print("DB error:", e)
        return 0

def get_watchlist_count(user_id: int) -> int:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM watchlist WHERE user_id=%s", (user_id,))
        return cur.fetchone()[0]
    except Exception as e:
        print("DB error:", e)
        return 0



def get_trending_movies(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, release_year, poster_url FROM movies
        ORDER BY release_year DESC
        LIMIT %s
    """, (limit,))  # Use a tuple for passing the limit as a parameter
    return cursor.fetchall()
