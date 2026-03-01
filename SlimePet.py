import sys
import random
import math
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QPointF
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QBrush, QPen, QScreen

APP_NAME = "SlimePet"
APP_VERSION = "v0.0.2"

class SlimePet(QWidget):
    active_pets = []

    def __init__(self, start_pos=None):
        super().__init__()
        
        # Window settings
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle(APP_NAME)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Core State
        self.base_size = 100
        self.scale_factor = 1.0
        self.growth_rate = 1.0015 # Grows smoothly every tick when H=1.0
        self.max_scale = 5.0
        self.tick_ms = 30
        self.split_after_ms = 60000
        self.max_hungry_elapsed_ms = 0
        
        self.hunger_level = 0.0 # 0.0 to 1.0
        # Hunger maxes out after ~60 seconds (60000ms)
        # 30ms tick rate => 60000/30 = 2000 ticks => 0.0005 per tick
        self.hunger_increase_rate = 0.0005
        
        self.time_val = 0.0 # for wobbly physics
        self.particles = [] # for angry smoke
        
        # 'crying' or 'angry' behavior when fully hungry
        self.temperament = random.choice(['crying', 'angry'])
        
        # Positioning
        self.current_pos = QPointF(100.0, 100.0)
        self.target_pos = QPointF(100.0, 100.0)
        self.base_speed = 1.3 # 30% faster than previous 1.0
        
        # Timers
        self.main_timer = QTimer(self)
        self.main_timer.timeout.connect(self.update_loop)
        self.main_timer.start(self.tick_ms) # ~33fps
        
        self.wandering_timer = QTimer(self)
        self.wandering_timer.timeout.connect(self.choose_new_target)
        # Timer started inside choose_new_target
        
        # Initialization
        self.update_window_size()
        if start_pos is None:
            self.center_on_screen()
        else:
            self.current_pos = QPointF(start_pos.x(), start_pos.y())
            self.target_pos = QPointF(start_pos.x(), start_pos.y())
            self.move(int(self.current_pos.x()), int(self.current_pos.y()))
        self.choose_new_target()
        SlimePet.active_pets.append(self)
        
    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.current_pos = QPointF(screen.width() / 2 - self.width() / 2, screen.height() / 2 - self.height() / 2)
        self.target_pos = self.current_pos
        self.move(int(self.current_pos.x()), int(self.current_pos.y()))
        
    def update_window_size(self):
        size = int(self.base_size * self.scale_factor)
        self.setFixedSize(size, size)
        
    def feed(self):
        if self.hunger_level > 0.0:
            self.hunger_level = 0.0
            self.max_hungry_elapsed_ms = 0
            
            # Reset size smoothly or instantly (Instantly for now)
            old_size = self.width()
            self.scale_factor = 1.0
            self.update_window_size()
            new_size = self.width()
            
            # Stay centered on shrink
            offset = (new_size - old_size) / 2
            self.current_pos.setX(self.current_pos.x() - offset)
            self.current_pos.setY(self.current_pos.y() - offset)
            self.target_pos.setX(self.target_pos.x() - offset)
            self.target_pos.setY(self.target_pos.y() - offset)
            
            # Reset temperament for next hunger cycle
            self.temperament = random.choice(['crying', 'angry'])
            self.particles = [] # Clear any existing smoke
            
            self.update()

    def spawn_clone(self):
        screen = QApplication.primaryScreen().availableGeometry()
        clone_size = self.base_size
        max_x = max(0, screen.width() - clone_size)
        max_y = max(0, screen.height() - clone_size)

        offset = clone_size + 20
        candidate_positions = [
            QPointF(self.current_pos.x() + offset, self.current_pos.y()),
            QPointF(self.current_pos.x() - offset, self.current_pos.y()),
            QPointF(self.current_pos.x(), self.current_pos.y() + offset),
            QPointF(self.current_pos.x(), self.current_pos.y() - offset),
        ]
        chosen = random.choice(candidate_positions)

        clone_x = min(max(0, chosen.x()), max_x)
        clone_y = min(max(0, chosen.y()), max_y)
        clone = SlimePet(start_pos=QPointF(clone_x, clone_y))
        clone.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.feed()
            # Clicking gives this widget keyboard focus so "q" can quit.
            self.setFocus()
            self.drag_pos = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_pos'):
            new_pos = event.globalPosition().toPoint() - self.drag_pos
            self.move(new_pos)
            self.current_pos = QPointF(new_pos.x(), new_pos.y())
            self.target_pos = self.current_pos
            event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            QApplication.quit()
            event.accept()
            return
        super().keyPressEvent(event)
            
    def choose_new_target(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.width()
        
        max_x = max(0, screen.width() - size)
        max_y = max(0, screen.height() - size)
        
        # Wander across the entire screen
        # 60% chance to target an edge/corner area to ensure sweeping movements
        if random.random() < 0.6:
            if random.random() < 0.5:
                new_x = random.choice([0, max_x])
                new_y = random.randint(0, max_y)
            else:
                new_x = random.randint(0, max_x)
                new_y = random.choice([0, max_y])
        else:
            new_x = random.randint(0, max_x)
            new_y = random.randint(0, max_y)
        
        self.target_pos = QPointF(new_x, new_y)
        self.wandering_timer.start(random.randint(15000, 45000))
        
        if random.random() < 0.1:
            self.target_pos = QPointF(self.current_pos.x(), self.current_pos.y())

    def update_loop(self):
        self.time_val += 0.15 # advance animation
        
        # Hunger progression
        if self.hunger_level < 1.0:
            self.hunger_level = min(1.0, self.hunger_level + self.hunger_increase_rate)
            self.max_hungry_elapsed_ms = 0
        else:
            # Fully hungry -> start growing
            if self.scale_factor < self.max_scale:
                old_size = self.width()
                self.scale_factor *= self.growth_rate
                self.update_window_size()
                new_size = self.width()
                offset = (new_size - old_size) / 2
                
                self.current_pos.setX(self.current_pos.x() - offset)
                self.current_pos.setY(self.current_pos.y() - offset)
                self.target_pos.setX(self.target_pos.x() - offset)
                self.target_pos.setY(self.target_pos.y() - offset)
            else:
                # If still not fed at max size, split every 1 minute repeatedly.
                self.max_hungry_elapsed_ms += self.tick_ms
                if self.max_hungry_elapsed_ms >= self.split_after_ms:
                    self.spawn_clone()
                    self.max_hungry_elapsed_ms = 0
                
            # Spawn angry smoke particles when fully hungry AND temperament is angry
            if self.temperament == 'angry' and random.random() < 0.3: # 30% chance per tick to spawn smoke
                pw = self.width() * random.uniform(0.1, 0.2)
                # Spawn roughly at the top of the head
                px = self.width() * 0.5 + random.uniform(-pw, pw)
                py = self.height() * 0.2
                self.particles.append({
                    'x': px, 'y': py, 'w': pw, 'life': 1.0, 
                    'vx': random.uniform(-1.0, 1.0), 'vy': random.uniform(-3.0, -1.0)
                })
        
        # Update particles
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        # Movement
        # Slow down slightly when fully hungry
        current_speed = self.base_speed * (1.0 - (self.hunger_level * 0.7)) 
        
        dx = self.target_pos.x() - self.current_pos.x()
        dy = self.target_pos.y() - self.current_pos.y()
        dist = math.hypot(dx, dy)
        
        if dist > current_speed:
            self.current_pos.setX(self.current_pos.x() + (dx / dist) * current_speed)
            self.current_pos.setY(self.current_pos.y() + (dy / dist) * current_speed)
            self.move(int(self.current_pos.x()), int(self.current_pos.y()))
        else:
            self.current_pos = QPointF(self.target_pos.x(), self.target_pos.y())
            self.move(int(self.current_pos.x()), int(self.current_pos.y()))
            # Arrived at destination early, occasionally pick a new target
            if random.random() < 0.05:
                self.choose_new_target()
            
        self.update() # trigger paint
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        H = self.hunger_level
        
        # Base opacity is ALWAYS 50%
        a = 128
        
        # Colors: Blue (Happy) -> Grey (Hungry) -> Red(Angry) / Grey(Crying)
        if H <= 0.5:
            # 0.0 to 0.5 maps to Blue -> Grey
            t = H * 2.0 # 0.0 to 1.0
            r = int(100 + (160 - 100) * t)
            g = int(180 + (160 - 180) * t)
            b = int(255 + (180 - 255) * t)
        else:
            # 0.5 to 1.0
            t = (H - 0.5) * 2.0 # 0.0 to 1.0
            if self.temperament == 'angry':
                # Grey -> Red
                r = int(160 + (255 - 160) * t)
                g = int(160 + (80 - 160) * t)
                b = int(180 + (80 - 180) * t)
            else:
                # Grey -> Stay Grey
                r = 160
                g = 160
                b = 180
        
        # Wobbly Physics based on time_val and scale
        # Reduce wobble slightly if hungry and tired
        wobble_mult = 1.0 - (H * 0.5) 
        wobble_x = math.sin(self.time_val) * (w * 0.05) * wobble_mult
        wobble_y = math.cos(self.time_val * 1.5) * (h * 0.04) * wobble_mult
        
        # Slime body dimensions (Very round, but slightly wide dumpling)
        cx = w * 0.5 + wobble_x * 0.5
        cy = h * 0.6 # Center
        rx = w * 0.45 # Wide radius
        ry_top = h * 0.4 - wobble_y # Round top
        ry_bottom = h * 0.3 + wobble_y * 0.5 # Round bottom
        
        kappa = 0.55228 # Bezier approximation for circles
        
        path = QPainterPath()
        # Start at top center
        path.moveTo(cx, cy - ry_top)
        
        # Top-center to Right-center (Tapered top for droplet look)
        path.cubicTo(cx + rx * 0.35, cy - ry_top,
                     cx + rx, cy - ry_top * kappa,
                     cx + rx, cy)
        
        # Right-center to Bottom-center (Smooth, rounded wide bottom)
        path.cubicTo(cx + rx, cy + ry_bottom * kappa,
                     cx + rx * kappa, cy + ry_bottom,
                     cx, cy + ry_bottom)
        
        # Bottom-center to Left-center
        path.cubicTo(cx - rx * kappa, cy + ry_bottom,
                     cx - rx, cy + ry_bottom * kappa,
                     cx - rx, cy)
        
        # Left-center to Top-center (Tapered top)
        path.cubicTo(cx - rx, cy - ry_top * kappa,
                     cx - rx * 0.35, cy - ry_top,
                     cx, cy - ry_top)
        
        painter.setBrush(QBrush(QColor(r, g, b, a)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        # Eyes
        eye_len = w * 0.035
        pen_width = max(2, int(w * 0.035))
        painter.setPen(QPen(QColor(30, 30, 40, int(255*(0.7+0.3*H))), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        
        cy = h * 0.6 + wobble_y * 0.3
        
        # Closer together, but not too close
        left_cx = w * 0.35 + wobble_x * 0.3
        right_cx = w * 0.65 + wobble_x * 0.3
        
        is_blinking = math.sin(self.time_val * 0.5) > 0.97 and H < 0.3
        
        if is_blinking:
            # Closed blink
            painter.drawLine(int(left_cx - eye_len), int(cy), int(left_cx + eye_len), int(cy))
            painter.drawLine(int(right_cx - eye_len), int(cy), int(right_cx + eye_len), int(cy))
        else:
            if H < 0.5:
                # Happy Eyes (^ ^)
                h_val = H * 2.0 # 0.0 to 1.0 (Happy to Neutral)
                
                # Left
                painter.drawLine(int(left_cx - eye_len), int(cy + eye_len * (1.0 - h_val)), int(left_cx), int(cy))
                painter.drawLine(int(left_cx), int(cy), int(left_cx + eye_len), int(cy + eye_len * (1.0 - h_val)))
                
                # Right
                painter.drawLine(int(right_cx - eye_len), int(cy + eye_len * (1.0 - h_val)), int(right_cx), int(cy))
                painter.drawLine(int(right_cx), int(cy), int(right_cx + eye_len), int(cy + eye_len * (1.0 - h_val)))
                
            elif H < 1.0 or self.temperament == 'crying':
                # Crying Eyes (T T) used for 0.5->1.0 (approaching hungry) 
                # AND also used for fully hungry if temperament == 'crying'
                
                # if fully hungry and crying, clamp tear width h_val to max
                h_val = min(1.0, (H - 0.5) * 2.0) 
                
                # Left
                # Horizontal slight droop
                painter.drawLine(int(left_cx - eye_len), int(cy - eye_len * 0.5), int(left_cx + eye_len), int(cy + eye_len * 0.5))
                # Tear lines (blue) if somewhat hungry
                painter.setPen(QPen(QColor(80, 150, 255, alpha=int(180 * h_val)), max(2, int(w*0.02)), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                painter.drawLine(int(left_cx), int(cy), int(left_cx), int(cy + eye_len * 2.5))
                
                # Right
                painter.setPen(QPen(QColor(30, 30, 40, int(255*(0.7+0.3*H))), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                painter.drawLine(int(right_cx - eye_len), int(cy + eye_len * 0.5), int(right_cx + eye_len), int(cy - eye_len * 0.5))
                painter.setPen(QPen(QColor(80, 150, 255, alpha=int(180 * h_val)), max(2, int(w*0.02)), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                painter.drawLine(int(right_cx), int(cy), int(right_cx), int(cy + eye_len * 2.5))
                
                # Restore pen for blush
                painter.setPen(QPen(QColor(30, 30, 40, int(255*(0.7+0.3*H))), pen_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

            elif self.temperament == 'angry':
                # Angry Eyes (\ /) used for fully hungry if temperament == 'angry'
                # Left
                painter.drawLine(int(left_cx - eye_len), int(cy - eye_len), int(left_cx + eye_len), int(cy + eye_len))
                # Right
                painter.drawLine(int(right_cx - eye_len), int(cy + eye_len), int(right_cx + eye_len), int(cy - eye_len))
            
        # Blush (Rimuru often has 2 small diagonal lines for blush when happy)
        if H < 0.8:
            blush_a = int(180 * (1.0 - H)) # More opaque blush when fully happy
            pen_w = max(1, int(w * 0.02))
            painter.setPen(QPen(QColor(255, 100, 150, blush_a), pen_w, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            
            # left cheek
            painter.drawLine(int(left_cx - w*0.1), int(cy + h*0.1), int(left_cx - w*0.07), int(cy + h*0.06))
            painter.drawLine(int(left_cx - w*0.06), int(cy + h*0.1), int(left_cx - w*0.03), int(cy + h*0.06))
            
            # right cheek
            painter.drawLine(int(right_cx + w*0.03), int(cy + h*0.1), int(right_cx + w*0.06), int(cy + h*0.06))
            painter.drawLine(int(right_cx + w*0.07), int(cy + h*0.1), int(right_cx + w*0.1), int(cy + h*0.06))
            
        # Draw Angry Smoke Particles
        if self.particles:
            painter.setPen(Qt.PenStyle.NoPen)
            for p in self.particles:
                # Grey, fading out
                alpha = int(255 * p['life'] * 0.6) # max 60% opacity
                painter.setBrush(QBrush(QColor(100, 100, 100, alpha)))
                # Size grows slightly as it dissipates
                size = p['w'] * (1.0 + (1.0 - p['life']) * 0.5)
                # Particles are drawn relative to the widget's coordinate system
                painter.drawEllipse(int(p['x'] - size/2), int(p['y'] - size/2), int(size), int(size))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = SlimePet()
    pet.show()
    sys.exit(app.exec())
