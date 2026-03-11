from deep_sort_realtime.deepsort_tracker import DeepSort

tracker = DeepSort()

def track_objects(detections, frame):
    # detections: list of [x1, y1, x2, y2, confidence, class]
    tracks = tracker.update_tracks(detections, frame=frame)
    # tracks: list of track objects with .track_id, .to_ltrb(), .det_class, .det_conf
    return tracks