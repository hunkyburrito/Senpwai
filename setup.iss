; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Senpwai"
#define MyAppVersion "2.0.7"
#define MyAppPublisher "AkatsuKi Inc."
#define MyAppURL "https://github.com/SenZmaKi/Senpwai"
#define MyAppExeName "Senpwai.exe"
#define ProjectRootDir "C:\Users\PC\OneDrive\Documents\Python\Senpwai"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B1AC746D-A6F0-44EF-B812-0D93F4571B51}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion=2.0.6.0
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
OutputDir={#ProjectRootDir}\setups
OutputBaseFilename=Senpwai-setup
SetupIconFile="{#ProjectRootDir}\src\assets\misc\senpwai-icon.ico"
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "{#ProjectRootDir}\build\Senpwai\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
; Delete the run on startup shortcut
Type: filesandordirs; Name: "{userstartup}\Senpwai.lnk"

[InstallDelete]
Type: filesandordirs; Name: "{app}"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall 
; [Code]
; var 
;  IsUpdate: Boolean;
; procedure AutoLaunch;
; begin
;   IsUpdate := ParamStr(2) = '/update';
;   if IsUpdate then
;   begin
;     Exec(ExpandConstant('{app}\{MyAppExeName}'), '', '', SW_SHOWNORMAL, ewNoWait, ResultCode);
;   end;
; end;