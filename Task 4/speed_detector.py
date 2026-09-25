import cv2
from ultralytics import YOLO

DISTANCE_M = 9.144


class SpeedLine:
    def __init__(self, x1, x2, y):
        self.x1 = x1
        self.x2 = x2
        self.y = y

    def is_crossed(self, cx, prev_y, cur_y):
        crossed = (prev_y < self.y <= cur_y) or (prev_y > self.y >= cur_y)
        return crossed and self.x1 <= cx <= self.x2


class Vehicle:
    def __init__(self, track_id):
        self.track_id = track_id
        self.prev_cy = None
        self.time_a = None
        self.time_b = None
        self.speed = None

    def update(self, cx, cy, frame_idx, line_a, line_b, fps):
        if self.prev_cy is not None:

            if self.time_a is None and line_a.is_crossed(cx, self.prev_cy, cy):
                self.time_a = frame_idx / fps

            if (
                self.time_a is not None
                and self.time_b is None
                and line_b.is_crossed(cx, self.prev_cy, cy)
            ):
                self.time_b = frame_idx / fps
                self.calculate_speed()

        self.prev_cy = cy

    def calculate_speed(self):
        if self.time_a is not None and self.time_b is not None:
            time_diff = self.time_b - self.time_a

            if time_diff > 0:
                speed_ms = DISTANCE_M / time_diff
                self.speed = speed_ms * 3.6

    def get_speed(self):
        return self.speed


class SpeedDetector:
    def __init__(self, model_path, video_path):
        self.model = YOLO(model_path)
        self.video_path = video_path

        self.line_a = SpeedLine(250, 1050, 300)
        self.line_b = SpeedLine(200, 1100, 450)

        self.vehicles = {}

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        print("VIDEO SIZE:", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "x", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        fps = cap.get(cv2.CAP_PROP_FPS)


        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            raise ValueError("Could not read video FPS")

        frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_idx += 1

            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                conf=0.2,
                verbose=False
            )

            boxes = results[0].boxes

            if boxes.id is not None:
                xyxy_list = boxes.xyxy.int().tolist()
                track_ids = boxes.id.int().tolist()

                for (x1, y1, x2, y2), track_id in zip(
                    xyxy_list, track_ids
                ):
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    if track_id not in self.vehicles:
                        self.vehicles[track_id] = Vehicle(track_id)

                    vehicle = self.vehicles[track_id]

                    vehicle.update(
                        cx,
                        cy,
                        frame_idx,
                        self.line_a,
                        self.line_b,
                        fps
                    )

                    speed = vehicle.get_speed()

                    label = f"ID: {track_id}"

                    if speed is not None:
                        label += f" | {speed:.1f} km/h"

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2
                    )

            cv2.line(
                frame,
                (self.line_a.x1, self.line_a.y),
                (self.line_a.x2, self.line_a.y),
                (255, 0, 0),
                2
            )

            cv2.line(
                frame,
                (self.line_b.x1, self.line_b.y),
                (self.line_b.x2, self.line_b.y),
                (0, 0, 255),
                2
            )

            cv2.imshow("Radar Speed Detector", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = SpeedDetector(
        model_path="best.pt",
        video_path="sample_video.mp4"
    )

    detector.run()