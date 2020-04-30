import sqlite3


class ClipperDb:
    def __init__(self):
        self.conn = sqlite3.connect("clipper.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS videos
             (id text, title text, original_url text, original_channel_url)"""
        )
        self.conn.commit()

    def save_video_info(self, video_id, title, original_url, original_channel_url):
        self.cursor.execute(
            "INSERT INTO videos VALUES (?,?,?,?)",
            (video_id, title, original_url, original_channel_url),
        )
        self.conn.commit()

    def get_video_info(self, video_id):
        rows = list(
            self.cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        )
        return rows[0]

    def __del__(self):
        self.cursor.close()
        self.conn.close()
