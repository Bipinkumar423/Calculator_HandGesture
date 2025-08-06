import cv2

class Button:
    def __init__(self, pos, size, value):
        self.pos = pos
        self.size = size
        self.value = value

    def draw(self, img, is_highlighted=False):
        x, y = self.pos
        color = (180, 220, 255) if is_highlighted else (255, 255, 255)  # Highlight effect

        # Shadow
        cv2.rectangle(img, (x + 3, y + 3), (x + self.size + 3, y + self.size + 3), (50, 50, 50), cv2.FILLED)
        # Button
        cv2.rectangle(img, (x, y), (x + self.size, y + self.size), color, cv2.FILLED)
        cv2.rectangle(img, (x, y), (x + self.size, y + self.size), (0, 0, 0), 2)

        # Text
        text_x = x + int(self.size / 3)
        text_y = y + int(self.size / 1.7)
        cv2.putText(img, self.value, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)

    def is_clicked(self, x, y):
        return self.pos[0] < x < self.pos[0] + self.size and self.pos[1] < y < self.pos[1] + self.size
