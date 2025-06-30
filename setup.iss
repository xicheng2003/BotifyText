; Inno Setup Script for BotifyText
; 注：以分号开头的行是注释

[Setup]
; 程序的唯一ID，建议使用GUID生成器生成一个新的
AppId={{A3D279C8-D56B-F48F-ED61-3655A0A08DED}}
AppName=BotifyText
AppVersion=1.0.0
AppPublisher=xicheng2003
AppPublisherURL=https://github.com/xicheng2003
AppSupportURL=https://github.com/xicheng2003/BotifyText
AppUpdatesURL=https://github.com/xicheng2003/BotifyText/releases
DefaultDirName={autopf}\BotifyText
DefaultGroupName=BotifyText
AllowNoIcons=yes
; 最终生成的安装包文件名
OutputBaseFilename=BotifyText_v1.0.0_setup
; 安装包的图标
SetupIconFile=assets\bot_logo.ico
; 压缩方式
Compression=lzma
SolidCompression=yes
; 安装向导的视觉样式
WizardStyle=modern

; --- 新增部分：将版本信息写入EXE文件属性 ---
; 这部分内容将显示在 setup.exe 的“属性 -> 详细信息”中
VersionInfoVersion=1.0.0
VersionInfoCompany=xicheng2003
VersionInfoDescription=BotifyText Installer
VersionInfoProductName=BotifyText
VersionInfoProductVersion=1.0.0
VersionInfoCopyright=Copyright (C) 2025 xicheng2003

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
; 如果需要中文，可以取消下面这行的注释
Name: "chinesesimp"; MessagesFile: "compiler:Languages\ChineseSimp.isl"

[Tasks]
; 让用户选择是否创建桌面快捷方式
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 这是最关键的一行：告诉Inno Setup去哪里找我们打包好的exe文件
; 请确保BotifyText.exe位于项目的dist文件夹下
Source: "dist\BotifyText.exe"; DestDir: "{app}"; Flags: ignoreversion
; 如果您的应用需要其他文件，也可以在这里添加
; 例如: Source: "path\to\your\file.dll"; DestDir: "{app}";

[Icons]
; 创建开始菜单快捷方式
Name: "{group}\BotifyText"; Filename: "{app}\BotifyText.exe"
; 创建桌面快捷方式（如果用户在Tasks中选择了）
Name: "{autodesktop}\BotifyText"; Filename: "{app}\BotifyText.exe"; Tasks: desktopicon

[Run]
; 安装完成后，让用户选择是否立即运行应用
Filename: "{app}\BotifyText.exe"; Description: "{cm:LaunchProgram,BotifyText}"; Flags: nowait postinstall skipifsilent
