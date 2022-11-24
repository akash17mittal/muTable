from sound_event import SoundEvent

def start_receving_tap_events_with_location(width, height, space_for_ui, tap_location_receiver_conn, sound_signal_sender_conn):
    while 1:
        tap_location_event = tap_location_receiver_conn.recv()
        if tap_location_event.locationX > (1 - space_for_ui)*width:
            print("UI Event Detected")
        else:
            print("Instrument Event Detected")
            sound_signal_sender_conn.send(SoundEvent(tap_location_event.intensity, tap_location_event.locationX, tap_location_event.locationY))
