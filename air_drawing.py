import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time


class AirCanvas:
    def __init__(self):
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Drawing variables
        self.drawing_points = deque(maxlen=1024)
        self.canvas = None
        self.drawing_color = (0, 255, 0)  # Green
        self.brush_thickness = 5

        # Thumb detection timing
        self.thumb_extended_start = None
        self.thumb_hold_duration = 0.5
        self.drawing_enabled = True

        # Color picker variables
        self.color_picker_open = False
        self.fist_start_time = None
        self.fist_hold_duration = 0.5
        self.colors = [
            (255, 0, 0),  # Blue
            (0, 128, 255),  # Orange
            (0, 255, 0),  # Green
            (0, 255, 128),  # Spring Green
            (255, 255, 0),  # Cyan
            (255, 0, 128),  # Pink
            (255, 0, 255),  # Magenta
            (128, 0, 255),  # Purple
            (0, 0, 255),  # Red
            (0, 128, 128),  # Olive
            (128, 128, 0),  # Teal
            (0, 255, 255),  # Yellow
            (255, 255, 255),  # White
            (128, 128, 128),  # Gray
            (0, 0, 0),  # Black (eraser)
        ]
        self.color_labels = ["Blue", "Orange", "Green", "Spring", "Cyan", "Pink", "Magenta",
                             "Purple", "Red", "Olive", "Teal", "Yellow", "White", "Gray", "Eraser"]

    def is_fist(self, hand_landmarks):
        """Check if hand is making a fist (all fingers closed)"""
        landmarks = hand_landmarks.landmark

        # Check if all fingertips are below their middle joints
        index_closed = landmarks[8].y > landmarks[6].y
        middle_closed = landmarks[12].y > landmarks[10].y
        ring_closed = landmarks[16].y > landmarks[14].y
        pinky_closed = landmarks[20].y > landmarks[18].y

        return index_closed and middle_closed and ring_closed and pinky_closed

    def is_index_finger_up(self, hand_landmarks):
        """Check if only index finger is pointing up (original V1 logic)"""
        landmarks = hand_landmarks.landmark

        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        index_up = index_tip.y < index_pip.y
        middle_down = middle_tip.y > middle_pip.y
        thumb_down = thumb_tip.y > thumb_ip.y

        return index_up and middle_down

    def is_thumb_extended(self, hand_landmarks):
        """Check if thumb is fully extended and distinctly far out"""
        landmarks = hand_landmarks.landmark

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        index_tip = landmarks[8]
        index_mcp = landmarks[5]

        # Calculate distance of thumb tip from palm center
        palm_center_x = (landmarks[0].x + landmarks[5].x + landmarks[17].x) / 3
        palm_center_y = (landmarks[0].y + landmarks[5].y + landmarks[17].y) / 3

        thumb_distance = np.sqrt((thumb_tip.x - palm_center_x) ** 2 + (thumb_tip.y - palm_center_y) ** 2)
        thumb_extension = np.sqrt((thumb_tip.x - thumb_ip.x) ** 2 + (thumb_tip.y - thumb_ip.y) ** 2)
        index_distance = np.sqrt((index_tip.x - index_mcp.x) ** 2 + (index_tip.y - index_mcp.y) ** 2)

        return thumb_distance > 0.2 and thumb_extension > index_distance * 0.6

    def update_drawing_state(self, hand_landmarks):
        """Update whether drawing is enabled based on thumb gesture timing"""
        if self.is_thumb_extended(hand_landmarks):
            if self.thumb_extended_start is None:
                self.thumb_extended_start = time.time()
            else:
                elapsed = time.time() - self.thumb_extended_start
                if elapsed >= self.thumb_hold_duration:
                    if elapsed < self.thumb_hold_duration + 0.1:
                        self.drawing_enabled = not self.drawing_enabled
                        status = "ENABLED" if self.drawing_enabled else "DISABLED"
                        print(f"Drawing {status}!")
        else:
            self.thumb_extended_start = None

    def update_color_picker_state(self, hand_landmarks):
        """Toggle color picker based on fist gesture"""
        if self.is_fist(hand_landmarks):
            if self.fist_start_time is None:
                self.fist_start_time = time.time()
            else:
                elapsed = time.time() - self.fist_start_time
                if elapsed >= self.fist_hold_duration:
                    if elapsed < self.fist_hold_duration + 0.1:
                        self.color_picker_open = not self.color_picker_open
                        status = "OPENED" if self.color_picker_open else "CLOSED"
                        print(f"Color picker {status}!")
        else:
            self.fist_start_time = None

    def draw_color_picker(self, frame):
        """Draw color picker panel on the frame at the top"""
        h, w, _ = frame.shape
        panel_height = 120
        panel_y = 10

        # Draw background panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, panel_y), (w - 10, panel_y + panel_height), (50, 50, 50), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Draw title
        cv2.putText(frame, "COLOR PICKER - Point to select", (20, panel_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Draw color swatches
        swatch_size = 50
        spacing = 8
        colors_per_row = 8
        start_x = 20

        for i, (color, label) in enumerate(zip(self.colors, self.color_labels)):
            row = i // colors_per_row
            col = i % colors_per_row

            x = start_x + col * (swatch_size + spacing)
            y = panel_y + 40 + row * (swatch_size + spacing + 15)

            # Draw swatch
            cv2.rectangle(frame, (x, y), (x + swatch_size, y + swatch_size), color, -1)
            cv2.rectangle(frame, (x, y), (x + swatch_size, y + swatch_size), (255, 255, 255), 2)

            # Highlight current color
            if color == self.drawing_color:
                cv2.rectangle(frame, (x - 3, y - 3), (x + swatch_size + 3, y + swatch_size + 3),
                              (0, 255, 0), 3)

            # Draw label below swatch
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.3, 1)[0]
            label_x = x + (swatch_size - label_size[0]) // 2
            cv2.putText(frame, label, (label_x, y + swatch_size + 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

        return start_x, panel_y + 40, swatch_size, spacing, colors_per_row

    def check_color_selection(self, finger_pos, picker_coords):
        """Check if finger is pointing at a color swatch"""
        start_x, start_y, swatch_size, spacing, colors_per_row = picker_coords
        fx, fy = finger_pos

        for i in range(len(self.colors)):
            row = i // colors_per_row
            col = i % colors_per_row

            x = start_x + col * (swatch_size + spacing)
            y = start_y + row * (swatch_size + spacing + 15)

            # Check if finger is within swatch bounds
            if x <= fx <= x + swatch_size and y <= fy <= y + swatch_size:
                self.drawing_color = self.colors[i]
                print(f"Color changed to: {self.color_labels[i]}")
                return True

        return False

    def get_finger_position(self, hand_landmarks, img_shape):
        """Get index finger tip position in pixel coordinates"""
        index_tip = hand_landmarks.landmark[8]
        h, w, _ = img_shape
        x = int(index_tip.x * w)
        y = int(index_tip.y * h)
        return (x, y)

    def run(self):
        """Main application loop"""
        cap = cv2.VideoCapture(0)

        # Set higher resolution for bigger screen
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        ret, frame = cap.read()
        if ret:
            self.canvas = np.zeros_like(frame)

        print("\n=== AIR DRAWING APP ===")
        print("Instructions:")
        print("- Point with INDEX FINGER to draw")
        print("- Hold FIST for 0.5s to open/close color picker")
        print("- Point at colors to select them")
        print("- Hold THUMB OUT for 0.5s to toggle drawing on/off")
        print("- Press 'C' to clear canvas")
        print("- Press 'S' to save drawing")
        print("- Press 'Q' to quit")
        print("========================\n")

        prev_point = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            drawing_active = False
            picker_coords = None

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

                    # Update color picker state
                    self.update_color_picker_state(hand_landmarks)

                    # Update drawing state (only if picker is closed)
                    if not self.color_picker_open:
                        self.update_drawing_state(hand_landmarks)

                    # If color picker is open, allow color selection
                    if self.color_picker_open:
                        if self.is_index_finger_up(hand_landmarks):
                            current_point = self.get_finger_position(hand_landmarks, frame.shape)
                            cv2.circle(frame, current_point, 10, (255, 255, 0), -1)
                    else:
                        # Normal drawing mode
                        if self.is_index_finger_up(hand_landmarks) and self.drawing_enabled:
                            drawing_active = True
                            current_point = self.get_finger_position(hand_landmarks, frame.shape)

                            cv2.circle(frame, current_point, 10, self.drawing_color, -1)

                            if prev_point is not None:
                                cv2.line(self.canvas, prev_point, current_point,
                                         self.drawing_color, self.brush_thickness)
                                cv2.line(frame, prev_point, current_point,
                                         self.drawing_color, self.brush_thickness)

                            prev_point = current_point
                        else:
                            prev_point = None

                    # Show fist hold progress
                    if self.fist_start_time is not None:
                        elapsed = time.time() - self.fist_start_time
                        progress = min(elapsed / self.fist_hold_duration, 1.0)
                        bar_width = int(200 * progress)
                        bar_y = 240 if self.color_picker_open else 90
                        cv2.rectangle(frame, (10, bar_y), (210, bar_y + 20), (50, 50, 50), -1)
                        cv2.rectangle(frame, (10, bar_y), (10 + bar_width, bar_y + 20), (255, 165, 0), -1)
                        cv2.putText(frame, "Hold fist...", (10, bar_y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    # Show thumb hold progress
                    if self.thumb_extended_start is not None:
                        elapsed = time.time() - self.thumb_extended_start
                        progress = min(elapsed / self.thumb_hold_duration, 1.0)
                        bar_width = int(200 * progress)
                        bar_y = 210 if self.color_picker_open else 60
                        cv2.rectangle(frame, (10, bar_y), (210, bar_y + 20), (50, 50, 50), -1)
                        cv2.rectangle(frame, (10, bar_y), (10 + bar_width, bar_y + 20), (0, 255, 255), -1)
                        cv2.putText(frame, "Hold thumb...", (10, bar_y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                prev_point = None
                self.thumb_extended_start = None
                self.fist_start_time = None

            # Draw color picker if open
            if self.color_picker_open:
                picker_coords = self.draw_color_picker(frame)
                # Check for color selection
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if self.is_index_finger_up(hand_landmarks):
                            finger_pos = self.get_finger_position(hand_landmarks, frame.shape)
                            self.check_color_selection(finger_pos, picker_coords)

            # Combine frame with canvas
            output = cv2.addWeighted(frame, 0.7, self.canvas, 0.3, 0)

            # Add status text
            if self.color_picker_open:
                status = "COLOR PICKER MODE"
                color = (255, 165, 0)
                status_y = 200
            elif self.drawing_enabled:
                status = "DRAWING" if drawing_active else "READY TO DRAW"
                color = (0, 255, 0) if drawing_active else (0, 255, 255)
                status_y = 30
            else:
                status = "DRAWING DISABLED"
                color = (0, 0, 255)
                status_y = 30

            cv2.putText(output, status, (10, status_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Show current color indicator
            if not self.color_picker_open:
                cv2.rectangle(output, (output.shape[1] - 70, 10), (output.shape[1] - 10, 70),
                              self.drawing_color, -1)
                cv2.rectangle(output, (output.shape[1] - 70, 10), (output.shape[1] - 10, 70),
                              (255, 255, 255), 2)

            cv2.imshow("Air Canvas", output)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('c'):
                self.canvas = np.zeros_like(frame)
                print("Canvas cleared!")
            elif key == ord('s'):
                filename = f"drawing_{np.random.randint(1000, 9999)}.png"
                cv2.imwrite(filename, self.canvas)
                print(f"Drawing saved as: {filename}")

        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()


if __name__ == "__main__":
    app = AirCanvas()
    app.run()