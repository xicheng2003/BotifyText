# run_desktop.py (最终修正版 - 精确匹配runJavaScript签名)

import sys
import threading
import logging
import os
from backend.app import create_app

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, 
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QGraphicsColorizeEffect
)
from PySide6.QtWebEngineWidgets import QWebEngineView
# --- 核心修改1：从QtWebEngineCore中导入 QWebEngineScript ---
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineScript
from PySide6.QtCore import QUrl, Qt, QSize, QEvent, QTimer, Slot
from PySide6.QtGui import QIcon, QColor
from PySide6.QtSvgWidgets import QSvgWidget

# --- 日志, Flask, resource_path, CustomTitleBar 等部分代码保持不变 ---
# ... (之前的 CustomTitleBar 类代码完全不变，直接复制过来) ...
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

class CustomTitleBar(QWidget):
    # ... (这个类的全部代码保持原样，无需改动) ...
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        layout = QHBoxLayout(self); layout.setContentsMargins(10, 0, 5, 0); layout.setSpacing(10)
        self.themes = {'light': {'text': '#202020', 'icon': '#404040', 'hover': '#E5E5E5', 'close_hover': '#E81123'},'dark':  {'text': '#CDD5E0', 'icon': '#A0A0A0', 'hover': 'rgba(255, 255, 255, 0.1)', 'close_hover': '#E81123'}}
        self.icon_widget = QSvgWidget(resource_path("assets/icons/bot.svg")); self.icon_widget.setFixedSize(22, 22)
        self.title_label = QLabel("BotifyText", self)
        self.minimize_button = QPushButton(self); self.maximize_button = QPushButton(self); self.close_button = QPushButton(self)
        self.minimize_icon = QIcon(resource_path("assets/icons/minimize.svg")); self.maximize_icon = QIcon(resource_path("assets/icons/maximize.svg")); self.restore_icon = QIcon(resource_path("assets/icons/restore.svg")); self.close_icon = QIcon(resource_path("assets/icons/close.svg"))
        self.minimize_button.setIcon(self.minimize_icon); self.maximize_button.setIcon(self.maximize_icon); self.close_button.setIcon(self.close_icon)
        for btn in [self.minimize_button, self.maximize_button, self.close_button]:
            btn.setIconSize(QSize(14, 14)); btn.setFixedSize(QSize(38, 28))
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.parent_window.close)
        layout.addWidget(self.icon_widget); layout.addWidget(self.title_label)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(self.minimize_button); layout.addWidget(self.maximize_button); layout.addWidget(self.close_button)
        self.setFixedHeight(48); self.update_theme('dark')
        self._mouse_press_pos = None; self._mouse_move_pos = None
    def mousePressEvent(self, event): self._mouse_press_pos=event.globalPosition().toPoint(); self._mouse_move_pos=event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self._mouse_press_pos is not None: self.parent_window.move(self.parent_window.pos() + (event.globalPosition().toPoint() - self._mouse_move_pos)); self._mouse_move_pos=event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event): self._mouse_press_pos=None; self._mouse_move_pos=None
    def toggle_maximize(self):
        if self.parent_window.isMaximized(): self.parent_window.showNormal()
        else: self.parent_window.showMaximized()
    def update_maximize_icon(self):
        if self.parent_window.isMaximized(): self.maximize_button.setIcon(self.restore_icon)
        else: self.maximize_button.setIcon(self.maximize_icon)
    def update_theme(self, theme_name='dark'):
        theme = self.themes.get(theme_name, self.themes['dark'])
        self.title_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {theme['text']};")
        button_style = f"QPushButton {{ background-color: transparent; border: none; border-radius: 5px; }} QPushButton:hover {{ background-color: {theme['hover']}; }}"
        self.minimize_button.setStyleSheet(button_style); self.maximize_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style + f"QPushButton:hover {{ background-color: {theme['close_hover']}; }}")
        for widget in [self.icon_widget, self.minimize_button, self.maximize_button, self.close_button]:
            effect = QGraphicsColorizeEffect(); effect.setColor(QColor(theme['icon'])); widget.setGraphicsEffect(effect)


# --- 主窗口 (已更新) ---
class MainWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        # ... (窗口基本设置不变) ...
        self.setWindowTitle("BotifyText")
        self.resize(1280, 800); self.setMinimumSize(940, 720)
        self.setWindowFlags(Qt.FramelessWindowHint); self.setAttribute(Qt.WA_TranslucentBackground)
        self.main_container = QWidget(); self.main_container.setObjectName("mainContainer")
        main_layout = QVBoxLayout(self.main_container); main_layout.setContentsMargins(1,1,1,1); main_layout.setSpacing(0)
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
        # --- 核心修改2：精确匹配(str, int, object)签名 ---
        # 我们传入 QWebEngineScript.MainWorld 作为那个 'int' 参数
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
        themes = {'light': {'bg': '#f1f5f9', 'border': '#e2e8f0'}, 'dark':  {'bg': '#020817', 'border': '#30363d'}}
        theme = themes.get(theme_name, themes['dark'])
        self.main_container.setStyleSheet(f"#mainContainer {{ background-color: {theme['bg']}; border-radius: 8px; border: 1px solid {theme['border']}; }}")
        self.title_bar.update_theme(theme_name)

# --- main 启动流程 (无需改动) ---
if __name__ == '__main__':
    log.info("应用启动...")
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    app = QApplication(sys.argv)
    window_url = f"http://127.0.0.1:{port}"
    main_window = MainWindow(window_url)
    main_window.show()
    sys.exit(app.exec())