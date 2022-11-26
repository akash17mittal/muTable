from sound_event import SoundEvent
from instruments.drums.drums import Drums
import time


def play_predefined_sound(width, height, projectionData):
    drums = Drums(width, height)
    pieces = drums.pieces
    highlighed_images = drums.get_highlighted_images()
    time_delay = 0.35
    for num_reps in range(2):
        for i in range(2):
            drums.play_sound_from_point(SoundEvent(0.1, pieces[2].shape.center[0], pieces[2].shape.center[1]))
            projectionData.update_pic(highlighed_images["Piece3"], "RGB")
            time.sleep(time_delay)
            drums.play_sound_from_point(SoundEvent(0.1, pieces[0].shape.center[0], pieces[0].shape.center[1]))
            projectionData.update_pic(highlighed_images["Piece1"], "RGB")
            time.sleep(time_delay)
        for i in range(2):
            drums.play_sound_from_point(SoundEvent(0.1, pieces[1].shape.center[0], pieces[1].shape.center[1]))
            projectionData.update_pic(highlighed_images["Piece2"], "RGB")
            time.sleep(time_delay)
            drums.play_sound_from_point(SoundEvent(0.1, pieces[0].shape.center[0], pieces[0].shape.center[1]))
            projectionData.update_pic(highlighed_images["Piece1"], "RGB")
            time.sleep(time_delay)

    projectionData.update_pic(drums.get_full_image_with_ui(), "RGB")


def start_receving_tap_events_with_location(width, height, space_for_ui, tap_location_receiver_conn,
                                            sound_signal_sender_conn, projectionData):
    while 1:
        tap_location_event = tap_location_receiver_conn.recv()
        if tap_location_event.locationX > (1 - space_for_ui) * width:
            play_predefined_sound(width, height, projectionData)
            print("UI Event Detected")
        else:
            print("Instrument Event Detected")
            sound_signal_sender_conn.send(
                SoundEvent(tap_location_event.intensity, tap_location_event.locationX, tap_location_event.locationY))
