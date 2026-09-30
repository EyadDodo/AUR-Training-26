import cv2
import matplotlib.pyplot as plt
import numpy as np


class ShapeDetectorVideoProcessor:

    def __init__(self, video_path: str):
        self.video_path = video_path

    @staticmethod
    def process_frame(frame):
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask_red1, mask_red2)

        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        kernel = np.ones((3, 3), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

        red_contours, _ = cv2.findContours(
            red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for cnt in red_contours:
            area = cv2.contourArea(cnt)
            if area > 400:
                perimeter = cv2.arcLength(cnt, True)
                if perimeter == 0:
                    continue
                circularity = (4 * np.pi * area) / (perimeter * perimeter)
                if circularity > 0.7:
                    cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 2)
                    M = cv2.moments(cnt)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        cv2.putText(
                            frame,
                            "Red Circle",
                            (cX - 40, cY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            2,
                        )

        blue_contours, _ = cv2.findContours(
            blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for cnt in blue_contours:
            area = cv2.contourArea(cnt)
            if area > 400:
                approx = cv2.approxPolyDP(
                    cnt, 0.04 * cv2.arcLength(cnt, True), True
                )
                if len(approx) == 4:
                    cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)
                    x, y, w, h = cv2.boundingRect(approx)
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.2:
                        cv2.putText(
                            frame,
                            "Blue Square",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 0, 0),
                            2,
                        )

        return frame

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)
            cv2.imshow("Subtask 2 - Shape Detection & Labeling", processed_frame)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


def run_subtask1(image_path: str):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return

    avg_filtered = cv2.blur(img, (5, 5))
    med_filtered = cv2.medianBlur(img, 5)
    gauss_filtered = cv2.GaussianBlur(img, (5, 5), 0)

    edges_orig = cv2.Canny(img, 100, 200)
    edges_avg = cv2.Canny(avg_filtered, 100, 200)
    edges_med = cv2.medianBlur(cv2.Canny(med_filtered, 100, 200), 1)
    edges_gauss = cv2.Canny(gauss_filtered, 100, 200)

    titles = [
        "Original Noisy",
        "Average Blur",
        "Median Blur",
        "Gaussian Blur",
        "Edges (Orig)",
        "Edges (Average)",
        "Edges (Median)",
        "Edges (Gaussian)",
    ]
    images = [
        img,
        avg_filtered,
        med_filtered,
        gauss_filtered,
        edges_orig,
        edges_avg,
        edges_med,
        edges_gauss,
    ]

    plt.figure(figsize=(12, 6))
    for i in range(8):
        plt.subplot(2, 4, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i], fontsize=10)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_subtask1("noisy_face.png")
    video_processor = ShapeDetectorVideoProcessor("thrown_shapes_noisy_30s.mp4")
    video_processor.run()