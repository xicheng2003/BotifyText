# backend/app.py (最终修正版，解决多页面静态资源问题)

import os
import sys
import logging
import threading
import webbrowser
from flask import Flask, send_from_directory, request 

project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root_path not in sys.path:
    sys.path.insert(0, project_root_path)

from backend import utils
from backend.config import SERVER_CONFIG, ROBOT_CONFIG, MOTION_CONFIG, LLM_CONFIG
from backend.robot_controller import RobotController
from backend.command_parser import CommandParser
from backend.routes import api_bp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(module)s] %(message)s')
log = logging.getLogger(__name__)

def create_app():
    static_dir = os.path.join(project_root_path, 'frontend', 'dist')
    
    log.info(f"Flask 静态文件目录设置为: {static_dir}")
    desktop_html_path = os.path.join(static_dir, 'src', 'desktop.html')
    web_html_path = os.path.join(static_dir, 'src', 'web.html')

    if not os.path.isdir(static_dir):
        log.critical(f"致命错误: 前端静态文件目录 '{static_dir}' 不存在。请先运行 'npm run build'。")
    elif not os.path.exists(desktop_html_path):
         log.critical(f"致命错误: 在 '{desktop_html_path}' 中找不到桌面版入口文件。")
    elif not os.path.exists(web_html_path):
         log.critical(f"致命错误: 在 '{web_html_path}' 中找不到网页版入口文件。")
    
    # 核心修改：移除 static_url_path=''，我们将手动处理所有路由
    app = Flask(__name__, static_folder=static_dir)

    app.config['robot_controller'] = RobotController(ROBOT_CONFIG, MOTION_CONFIG)
    app.config['command_parser'] = CommandParser(LLM_CONFIG)
    app.config['SERVER_PORT'] = SERVER_CONFIG.get('port', 5000)
    app.register_blueprint(api_bp)

    # --- Vue前端服务路由 (全新、更稳健的版本) ---
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue_app(path):
        # 检查请求的路径是否直接对应于dist目录下的一个真实文件
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        
        # 如果不是真实文件，则判断是哪个单页面应用的路由
        if request.path.startswith('/web'):
            # 所有以/web开头的路径都返回web版入口
            log.info(f"为Web浏览器路径 '{request.path}' 提供UI (src/web.html)")
            return send_from_directory(os.path.join(app.static_folder, 'src'), 'web.html')
        else:
            # 其他所有路径都返回桌面版入口
            log.info(f"为桌面应用路径 '{request.path}' 提供UI (src/desktop.html)")
            return send_from_directory(os.path.join(app.static_folder, 'src'), 'desktop.html')

    return app

# --- 启动逻辑 (恢复此部分，以便直接运行测试) ---
if __name__ == '__main__':
    app = create_app()
    host = SERVER_CONFIG.get('host', '0.0.0.0')
    port = SERVER_CONFIG.get('port', 5000)
    
    log.info(f"Flask后端服务独立启动（仅供测试），将在 http://{host}:{port} 上运行...")
    app.run(host=host, port=port, debug=False)
