; Minimal NSIS Installer Script for MSR605 Card Reader/Writer

; --------------------------------
; Version Information
; --------------------------------
!define MAJOR_VERSION "2"
!define MINOR_VERSION "4"
!define PATCH_VERSION "0"
!define BUILD_NUMBER "0"
!define VERSION "${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}.${BUILD_NUMBER}"
!define APPNAME "MSR605"
!define DISPLAY_NAME "MSR605 Card Reader/Writer"
!define PUBLISHER "Nsfr750"
!define COMPANY "Nsfr750"
!define WEBSITE "https://github.com/Nsfr750/MSR605"
!define UPDATE_URL "${WEBSITE}/releases/latest"
!define HELP_URL "${WEBSITE}/wiki"
!define SUPPORT_EMAIL "nsfr750@yandex.com"
!define DISCORD_URL "https://discord.gg/BvvkUEP9"

; --------------------------------
; Version Info for the installer
; --------------------------------
VIProductVersion "${VERSION}"
VIAddVersionKey "ProductName" "${DISPLAY_NAME}"
VIAddVersionKey "CompanyName" "${COMPANY}"
VIAddVersionKey "LegalCopyright" "© 2025 ${PUBLISHER}"
VIAddVersionKey "FileDescription" "${DISPLAY_NAME} Installer"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "ProductVersion" "${VERSION}"
VIAddVersionKey "InternalName" "${APPNAME}"
VIAddVersionKey "OriginalFilename" "${APPNAME}-v${VERSION}-Setup.exe"
VIAddVersionKey "ProductVersionString" "${VERSION}"

; Variables
Var CreateDesktopSC
Var AssocImages
Var ReinstallUninstallString

; Modern UI
!include "MUI2.nsh"

; General settings
Name "${APPNAME}"
OutFile "..\dist\${APPNAME}-v${VERSION}-Setup.exe"
InstallDir "$PROGRAMFILES64\${APPNAME}"
InstallDirRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation"
RequestExecutionLevel admin

; UI settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-uninstall.ico"

; Header Images
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\orange.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\orange-uninstall-r.bmp"
!define MUI_HEADERIMAGE_RIGHT

; Welcome/Finish page
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"
!define MUI_WELCOMEFINISHPAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange-uninstall.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"

; Other UI settings
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

; Modern UI2 settings
!define MUI_UI_HEADERIMAGE_RIGHT "${NSISDIR}\Contrib\UIs\modern_headerbmp.exe"
!define MUI_UI_COMPONENTSPAGE_SMALLDESC
!define MUI_UI_HEADERIMAGE

; Add support for Windows 10/11 DPI awareness
!include "WinVer.nsh"
!include "x64.nsh"

; Request DPI awareness for the installer
ManifestDPIAware true

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Italian"

Function .onInit
  ; Initialize variables
  StrCpy $CreateDesktopSC 0
  StrCpy $AssocImages 0
  
  ; Check if source files exist before installation
  IfFileExists "X:\GitHub\MSR605\MSR605.exe" exe_found
    MessageBox MB_OK|MB_ICONSTOP "Error: MSR605.exe not found at X:\GitHub\MSR605\MSR605.exe"
    Abort
  exe_found:
  
  IfFileExists "X:\GitHub\MSR605\assets\*.*" assets_found
    MessageBox MB_OK|MB_ICONEXCLAMATION "Warning: assets directory not found at X:\GitHub\MSR605\assets"
  assets_found:
  
  IfFileExists "X:\GitHub\MSR605\README.md" readme_found
    MessageBox MB_OK|MB_ICONEXCLAMATION "Warning: README.md not found at X:\GitHub\MSR605\README.md"
  readme_found:
  
  IfFileExists "X:\GitHub\MSR605\LICENSE" license_found
    MessageBox MB_OK|MB_ICONEXCLAMATION "Warning: LICENSE not found at X:\GitHub\MSR605\LICENSE"
  license_found:
  
  IfFileExists "X:\GitHub\MSR605\CHANGELOG.md" changelog_found
    MessageBox MB_OK|MB_ICONEXCLAMATION "Warning: CHANGELOG.md not found at X:\GitHub\MSR605\CHANGELOG.md"
  changelog_found:
  
  ; Check for previous installation
  ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString"
  StrCmp $R0 "" done
  
  ; If previous installation found, show message
  MessageBox MB_YESNO|MB_ICONQUESTION "${APPNAME} is already installed. $\n$\nDo you want to uninstall the previous version before continuing with the installation?" IDYES uninst
  Abort
  
  uninst:
    ClearErrors
    ExecWait '$R0 _?=$INSTDIR'
    IfErrors no_remove_uninstaller
    Delete $R0
    RMDir $INSTDIR
    
  no_remove_uninstaller:
    IfErrors no_remove_folder
    RMDir /r $INSTDIR
    
  no_remove_folder:
    IfErrors +2
    Delete "$DESKTOP\${APPNAME}.lnk"
    
  done:
FunctionEnd

; Installer section
Section "MainSection" SecMain
  ; Set output directory
  SetOutPath "$INSTDIR"
  
  ; Add the main executable with verification
  SetOutPath "$INSTDIR"
  File "X:\GitHub\MSR605\dist\MSR605.exe"
  IfFileExists "$INSTDIR\MSR605.exe" +5
    MessageBox MB_OK|MB_ICONSTOP "Failed to install MSR605.exe to $INSTDIR"
    MessageBox MB_OK|MB_ICONINFORMATION "Current directory: $EXEDIR"
    MessageBox MB_OK|MB_ICONINFORMATION "Source file exists: $\nX:\GitHub\MSR605\dist\MSR605.exe"
    Abort
  
  ; Add assets directory with detailed error checking
  IfFileExists "X:\GitHub\MSR605\assets\*.*" assets_exist
    MessageBox MB_OK|MB_ICONEXCLAMATION "Skipping assets: Source directory not found at X:\GitHub\MSR605\assets"
    Goto skip_assets
  
  assets_exist:
  CreateDirectory "$INSTDIR\assets"
  IfFileExists "$INSTDIR\assets" +3
    MessageBox MB_OK|MB_ICONSTOP "Failed to create directory: $INSTDIR\assets"
    Goto skip_assets
  
  SetOutPath "$INSTDIR\assets"
  File /r "X:\GitHub\MSR605\assets\*.*"
  IfFileExists "$INSTDIR\assets\*.*" assets_installed
    MessageBox MB_OK|MB_ICONSTOP "Failed to install assets to $INSTDIR\assets"
    Goto skip_assets
    
  assets_installed:
  MessageBox MB_OK|MB_ICONINFORMATION "Assets successfully installed to $INSTDIR\assets"
  
  skip_assets:
  
  ; Set output path back to installation directory
  SetOutPath "$INSTDIR"
  
  ; Add documentation files with detailed verification
  SetOutPath "$INSTDIR"
  
  ; Install README.md
  IfFileExists "X:\GitHub\MSR605\README.md" readme_exists
    MessageBox MB_OK|MB_ICONEXCLAMATION "Skipping README.md: Source file not found at X:\GitHub\MSR605\README.md"
    Goto skip_readme
  
  readme_exists:
  File "X:\GitHub\MSR605\README.md"
  IfFileExists "$INSTDIR\README.md" readme_installed
    MessageBox MB_OK|MB_ICONSTOP "Failed to install README.md to $INSTDIR"
    Goto skip_readme
  
  readme_installed:
  MessageBox MB_OK|MB_ICONINFORMATION "Successfully installed README.md to $INSTDIR"
  
  skip_readme:
  
  ; Install LICENSE
  IfFileExists "X:\GitHub\MSR605\LICENSE" license_exists
    MessageBox MB_OK|MB_ICONEXCLAMATION "Skipping LICENSE: Source file not found at X:\GitHub\MSR605\LICENSE"
    Goto skip_license
  
  license_exists:
  File "X:\GitHub\MSR605\LICENSE"
  IfFileExists "$INSTDIR\LICENSE" license_installed
    MessageBox MB_OK|MB_ICONSTOP "Failed to install LICENSE to $INSTDIR"
    Goto skip_license
  
  license_installed:
  MessageBox MB_OK|MB_ICONINFORMATION "Successfully installed LICENSE to $INSTDIR"
  
  skip_license:
  
  ; Install CHANGELOG.md
  IfFileExists "X:\GitHub\MSR605\CHANGELOG.md" changelog_exists
    MessageBox MB_OK|MB_ICONEXCLAMATION "Skipping CHANGELOG.md: Source file not found at X:\GitHub\MSR605\CHANGELOG.md"
    Goto skip_changelog
  
  changelog_exists:
  File "X:\GitHub\MSR605\CHANGELOG.md"
  IfFileExists "$INSTDIR\CHANGELOG.md" changelog_installed
    MessageBox MB_OK|MB_ICONSTOP "Failed to install CHANGELOG.md to $INSTDIR"
    Goto skip_changelog
  
  changelog_installed:
  MessageBox MB_OK|MB_ICONINFORMATION "Successfully installed CHANGELOG.md to $INSTDIR"
  
  skip_changelog:
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Create start menu shortcut
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  
  ; Add/Remove Programs entry
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "DisplayVersion" "${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "Publisher" "${PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "URLInfoAbout" "${WEBSITE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "HelpLink" "${WEBSITE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "URLUpdateInfo" "${WEBSITE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "NoRepair" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "NoModify" 1
  
  ; Set a fixed estimated size (in KB)
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "EstimatedSize" 10240
  
  ; Create uninstaller for the current user
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "DisplayName" "${APPNAME}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "UninstallString" '"$INSTDIR\Uninstall.exe" /currentuser'
  
  ; Set file associations if selected
  ${If} $AssocImages == 1
    WriteRegStr HKCR ".jpg\OpenWithProgids" "${APPNAME}.jpg" ""
    WriteRegStr HKCR "${APPNAME}.jpg" "" "${APPNAME} Image"
    WriteRegStr HKCR "${APPNAME}.jpg\DefaultIcon" "" "$INSTDIR\${APPNAME}.exe,0"
    WriteRegStr HKCR "${APPNAME}.jpg\shell\open\command" "" '"$INSTDIR\${APPNAME}.exe" "%1"'
    
    ; Repeat for other image formats
    WriteRegStr HKCR ".jpeg\OpenWithProgids" "${APPNAME}.jpeg" ""
    WriteRegStr HKCR ".png\OpenWithProgids" "${APPNAME}.png" ""
    WriteRegStr HKCR ".bmp\OpenWithProgids" "${APPNAME}.bmp" ""
    WriteRegStr HKCR ".gif\OpenWithProgids" "${APPNAME}.gif" ""
    WriteRegStr HKCR ".tiff\OpenWithProgids" "${APPNAME}.tiff" ""
    WriteRegStr HKCR ".tif\OpenWithProgids" "${APPNAME}.tif" ""
    WriteRegStr HKCR ".webp\OpenWithProgids" "${APPNAME}.webp" ""
    
    ; Refresh shell
    System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
  ${EndIf}
  
  ; Register uninstaller with Windows
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
SectionEnd

; Optional section for desktop shortcut
Section /o "Desktop Shortcut" SecDesktopShortcut
  StrCpy $CreateDesktopSC 1
SectionEnd

; Optional section for file associations
Section /o "Associate Image Files" SecFileAssoc
  StrCpy $AssocImages 1
SectionEnd

; --------------------------------
; Custom Pages
; --------------------------------
Function PageReinstall
  ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString"
  StrCmp $R0 "" done
  
  StrCpy $ReinstallUninstallString $R0
  
  ; Simple message box for reinstallation prompt
  MessageBox MB_YESNO|MB_ICONQUESTION "${APPNAME} is already installed. Uninstall previous version?" IDYES uninstall_previous
  Abort
  
  uninstall_previous:
  StrCpy $0 "$ReinstallUninstallString"
  ExecWait '$0 /S _?=$INSTDIR'
  Delete "$0"
  RMDir "$INSTDIR"
  
  done:
FunctionEnd

Function PageLeaveReinstall
  ; No action needed here since we handle uninstallation in PageReinstall
  ; with a simple message box prompt
FunctionEnd

; --------------------------------
; Uninstaller Section
; --------------------------------
Section "Uninstall"
  ; Remove files and directories
  Delete "$INSTDIR\Uninstall.exe"
  
  ; Remove main executable
  Delete "$INSTDIR\${APPNAME}.exe"
  
  ; Remove documentation files
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\CHANGELOG.md"
  
  ; Remove assets directory
  RMDir /r "$INSTDIR\assets"
  
  ; Remove installation directory if empty
  RMDir "$INSTDIR"
  
  ; Remove start menu shortcuts
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APPNAME}"
  
  ; Remove desktop shortcut if it exists
  Delete "$DESKTOP\${APPNAME}.lnk"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
  
  ; Remove any file associations
  DeleteRegKey HKCR "Applications\${APPNAME}.exe"
  
  ; Notify the shell that we removed an application
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
  
  ; Show completion message
  MessageBox MB_ICONINFORMATION|MB_OK "${APPNAME} was successfully removed from your computer."
  
  ; Remove registry keys
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
  DeleteRegKey HKLM "Software\${APPNAME}"
  
  ; Remove file associations
  DeleteRegKey HKCR "${APPNAME}.jpg"
  DeleteRegKey HKCR "${APPNAME}.jpeg"
  DeleteRegKey HKCR "${APPNAME}.png"
  DeleteRegKey HKCR "${APPNAME}.bmp"
  DeleteRegKey HKCR "${APPNAME}.gif"
  DeleteRegKey HKCR "${APPNAME}.tiff"
  DeleteRegKey HKCR "${APPNAME}.tif"
  DeleteRegKey HKCR "${APPNAME}.webp"
  
  ; Refresh shell
  System::Call 'shell32.dll::SHChangeNotify(i, i, i, i) v (0x08000000, 0, 0, 0)'
  
SectionEnd

; --------------------------------
; Functions
; --------------------------------
; Note: The .onInit function is already defined at the beginning of the file

Function LaunchApplication
  ExecShell "" "$INSTDIR\${APPNAME}.exe"
FunctionEnd
