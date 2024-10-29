from pydbus import SessionBus
import time
from discordrp import Presence

session_bus = SessionBus()

amarok_mpris = session_bus.get("org.kde.amarok", "/MainApplication")
amarok_version = amarok_mpris.GetAll("")["applicationVersion"]

client_id = "1300779919214776340"

class AmarokRichPresence():
    def __init__(self):
        super().__init__()
        self.displayTrack()

    def displayTrack(self):
        with Presence(client_id) as presence:
            print("Connected to Discord")

            while True:
                current_track_info = self.getCurrentTrackInfo()
                
                if current_track_info:
                    status = current_track_info["status"]

                    if status == "Playing":
                        status_image = "play"
                    elif status == "Paused":
                        status_image = "pause"

                    position = current_track_info["position"]
                    duration = current_track_info["duration"]

                    artist = current_track_info["artist"]
                    title = current_track_info["title"]
                    album = current_track_info["album"]

                    time_start = int(time.time() - position)
                    time_end = int(time.time() + duration - position)

                    if status == "Playing":
                        timestamps = {
                            "start": time_start,
                            "end": time_end
                        }
                    else:
                        timestamps = {}

                    presence.set(
                        {
                            "state": f"from album: {album}",
                            "details": f"{artist} - {title}",
                            "timestamps": timestamps,
                            "assets": {
                                "large_image": "amarok",
                                "large_text": f"Amarok {amarok_version} (https://github.com/sech1p/AmarokRichPresence)",
                                "small_image": status_image,
                                "small_text": status
                            }
                        }
                    )
                else:
                    presence.set(
                        {
                            "details": "No music playing",
                            "assets": {
                                "large_image": "amarok",
                                "large_text": f"Amarok {amarok_version} (https://github.com/sech1p/AmarokRichPresence)",
                                "small_image": "stop",
                                "small_text": "Stopped"
                            }
                        }
                    )

                time.sleep(5)
    
    def getCurrentTrackInfo(self):
        amarok_player_mpris = session_bus.get("org.kde.amarok", "/org/mpris/MediaPlayer2")
        amarok_objects = amarok_player_mpris.GetAll("")

        status = amarok_objects["PlaybackStatus"]
        if status == "Playing" or status == "Paused":
            position = amarok_objects["Position"] / 1000000 # Convert from microseconds to seconds
            metadata = amarok_objects["Metadata"]

            return {
                "artist": metadata["xesam:artist"][0],
                "album": metadata["xesam:album"],
                "title": metadata["xesam:title"],
                "status": status,
                "position": position,
                "duration": metadata["mpris:length"] / 1000000 # Convert from microseconds to seconds
            }

script = AmarokRichPresence()
