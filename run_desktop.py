# run_desktop.py (具备优化主题和样式的最终版)

import sys
import threading
import logging
import os
from backend.app import create_app

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, 
    QPushButton, QLabel, QSpacerItem, QSizePolicy
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineScript
from PySide6.QtCore import QUrl, Qt, QSize, QEvent, QTimer, Slot
# --- 核心修改：导入QPainter和QPixmap用于重新绘制图标 ---
from PySide6.QtGui import QIcon, QColor, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


# --- 日志, Flask, resource_path 等部分代码保持不变 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(module)s] %(message)s')
log = logging.getLogger(__name__)
flask_app = create_app()
port = flask_app.config.get('SERVER_PORT', 5000)
def run_flask_server():
    flask_app.run(host='0.0.0.0', port=port, use_reloader=False)

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- 新增：一个辅助函数，用于创建带颜色的图标 ---
def create_tinted_icon(svg_path, color):
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(renderer.defaultSize())
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return QIcon(pixmap)

# --- 自定义标题栏组件 (已更新) ---
class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(10)

        self.themes = {
            'light': {'text': '#0F172A', 'icon': '#475569', 'hover': '#F1F5F9', 'close_hover': '#EF4444'},
            'dark':  {'text': '#E2E8F0', 'icon': '#94A3B8', 'hover': '#1E293B', 'close_hover': '#DC2626'}
        }
        
        # --- 核心修改：使用QLabel来显示可变色的主图标 ---
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(22, 22)
        self.title_label = QLabel("BotifyText", self)
        
        self.minimize_button = QPushButton(self)
        self.maximize_button = QPushButton(self)
        self.close_button = QPushButton(self)

        for btn in [self.minimize_button, self.maximize_button, self.close_button]:
            btn.setIconSize(QSize(14, 14))
            btn.setFixedSize(QSize(38, 28))

        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.parent_window.close)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        self.setFixedHeight(48)
        
        self.update_theme('dark')

        self._mouse_press_pos = None; self._mouse_move_pos = None
    def mousePressEvent(self, event): self._mouse_press_pos=event.globalPosition().toPoint(); self._mouse_move_pos=event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self._mouse_press_pos is not None: self.parent_window.move(self.parent_window.pos() + (event.globalPosition().toPoint() - self._mouse_move_pos)); self._mouse_move_pos=event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event): self._mouse_press_pos=None; self._mouse_move_pos=None
    def toggle_maximize(self):
        if self.parent_window.isMaximized(): self.parent_window.showNormal()
        else: self.parent_window.showMaximized()
        
    def update_maximize_icon(self):
        if self.parent_window.isMaximized():
            self.maximize_button.setIcon(self.themed_restore_icon)
        else:
            self.maximize_button.setIcon(self.themed_maximize_icon)

    def update_theme(self, theme_name='dark'):
        theme = self.themes.get(theme_name, self.themes['dark'])
        icon_color = theme['icon']
        
        self.title_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {theme['text']};")
        
        button_style = f"QPushButton {{ background-color: transparent; border: none; border-radius: 5px; }} QPushButton:hover {{ background-color: {theme['hover']}; }}"
        self.minimize_button.setStyleSheet(button_style)
        self.maximize_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style + f"QPushButton:hover {{ background-color: {theme['close_hover']}; }}")

        # --- 核心修改：使用新的辅助函数来创建并设置所有图标 ---
        # 主图标
        bot_pixmap = create_tinted_icon(resource_path("assets/icons/bot.svg"), icon_color).pixmap(22, 22)
        self.icon_label.setPixmap(bot_pixmap)
        
        # 按钮图标
        self.themed_minimize_icon = create_tinted_icon(resource_path("assets/icons/minimize.svg"), icon_color)
        self.themed_maximize_icon = create_tinted_icon(resource_path("assets/icons/maximize.svg"), icon_color)
        self.themed_restore_icon = create_tinted_icon(resource_path("assets/icons/restore.svg"), icon_color)
        self.themed_close_icon = create_tinted_icon(resource_path("assets/icons/close.svg"), icon_color)
        
        self.minimize_button.setIcon(self.themed_minimize_icon)
        self.close_button.setIcon(self.themed_close_icon)
        self.update_maximize_icon() # 更新最大化/恢复图标

# --- 主窗口 (MainWindow) 和 main 启动流程保持不变 ---
class MainWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("BotifyText")
        # --- 核心修改：在这里设置窗口图标 ---
        self.setWindowIcon(QIcon(resource_path("assets/bot_logo.ico")))
        
        self.resize(1280, 800)
        self.setMinimumSize(940, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_container = QWidget()
        self.main_container.setObjectName("mainContainer")
        main_layout = QVBoxLayout(self.main_container)
        main_layout.setContentsMargins(1, 1, 1, 1); main_layout.setSpacing(0)
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        self.browser = QWebEngineView()
        self.browser.page().setBackgroundColor(Qt.transparent)
        self.browser.setUrl(QUrl(url))
        main_layout.addWidget(self.browser)
        self.setCentralWidget(self.main_container)
        self.current_theme = 'dark'
        self.update_theme(self.current_theme)
        self.theme_checker = QTimer(self)
        self.theme_checker.setInterval(200)
        self.theme_checker.timeout.connect(self.check_frontend_theme)
        self.theme_checker.start()
    def check_frontend_theme(self):
        js_script = "document.documentElement.classList.contains('dark')"
        self.browser.page().runJavaScript(js_script, QWebEngineScript.MainWorld, self.handle_theme_result)
    @Slot(object)
    def handle_theme_result(self, is_dark):
        new_theme = 'dark' if is_dark else 'light'
        if new_theme != self.current_theme:
            log.info(f"检测到主题变化: {self.current_theme} -> {new_theme}")
            self.current_theme = new_theme
            self.update_theme(self.current_theme)
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.title_bar.update_maximize_icon()
        super().changeEvent(event)
    def update_theme(self, theme_name='dark'):
        themes = {'light': {'bg': '#FFFFFF', 'border': '#E2E8F0'},'dark':  {'bg': '#020817', 'border': '#1E293B'}}
        theme = themes.get(theme_name, themes['dark'])
        self.main_container.setStyleSheet(f"#mainContainer {{ background-color: {theme['bg']}; border-radius: 8px; border: 1px solid {theme['border']}; }}")
        self.title_bar.update_theme(theme_name)
if __name__ == '__main__':
    log.info("应用启动...")
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    app = QApplication(sys.argv)
    window_url = f"http://127.0.0.1:{port}"
    main_window = MainWindow(window_url)
    main_window.show()
    sys.exit(app.exec())
