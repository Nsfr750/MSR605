; NSIS Installer Script for MSR605 Card Reader/Writer
; Auto-generated with enhanced features for MSR605 Project

; Include Modern UI and other required libraries
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"
!include "WordFunc.nsh"
!include "WinVer.nsh"
!include "nsDialogs.nsh"
!include "Sections.nsh"

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
; Installer Attributes
; --------------------------------
Name "${DISPLAY_NAME}"
OutFile "..\dist\${APPNAME}-v${VERSION}-Setup.exe"
InstallDir "$PROGRAMFILES64\${APPNAME}"
InstallDirRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation"
RequestExecutionLevel admin
ShowInstDetails show
ShowUninstDetails show
BrandingText "${DISPLAY_NAME} v${VERSION}"

; Compression settings
SetCompressor /SOLID lzma
SetCompressorDictSize 64

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

; --------------------------------
; Interface Settings
; --------------------------------
!define MUI_ABORTWARNING
!define MUI_ICON "..\assets\icon.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Header Images
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\win.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\win-uninstall.bmp"
!define MUI_HEADERIMAGE_RIGHT

; Welcome/Finish page
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"
!define MUI_WELCOMEFINISHPAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win-uninstall.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"

; Other UI settings
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_UNFINISHPAGE_NOAUTOCLOSE
!define MUI_ICON "..\assets\icon.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Modern UI2 settings
!define MUI_UI_HEADERIMAGE_RIGHT "${NSISDIR}\Contrib\UIs\modern_headerbmp.exe"
!define MUI_UI_COMPONENTSPAGE_SMALLDESC
!define MUI_UI_HEADERIMAGE

; Add support for Windows 10/11 DPI awareness
!include "WinVer.nsh"
!include "x64.nsh"

; Request DPI awareness for the installer
ManifestDPIAware true

; --------------------------------
; Pages
; --------------------------------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

; Custom page to confirm installation
Page custom PageReinstall PageLeaveReinstall

; Include nsDialogs for custom pages
!include "nsDialogs.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"
!include "WinVer.nsh"
!include "x64.nsh"
!include "WordFunc.nsh"
!insertmacro VersionCompare

; Variables
Var ReinstallUninstallString
Var CreateDesktopSC
Var CreateStartMenuSC
Var InstallForAllUsers

!insertmacro MUI_PAGE_INSTFILES

; Custom finish page with more options
!define MUI_FINISHPAGE_TITLE "Installation Complete"
!define MUI_FINISHPAGE_TEXT "${DISPLAY_NAME} has been installed on your computer.\n\nThank you for choosing ${DISPLAY_NAME}!"
!define MUI_FINISHPAGE_RUN "$INSTDIR\\${APPNAME}.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${DISPLAY_NAME}"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchApplication"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\\README.md"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "View README"
!define MUI_FINISHPAGE_LINK "Visit ${DISPLAY_NAME} on GitHub"
!define MUI_FINISHPAGE_LINK_LOCATION "${WEBSITE}"
!define MUI_FINISHPAGE_NOREBOOTSUPPORT

; Add a custom finish page action
!define MUI_PAGE_CUSTOMFUNCTION_SHOW FinishPageShow
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE FinishPageLeave
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; --------------------------------
; Languages
; --------------------------------
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Italian"

; --------------------------------
; Variables
; --------------------------------
Var ReinstallUninstallString
Var CreateDesktopSC
Var AssocImages

; --------------------------------
; Installer Sections
; --------------------------------
Section "!${APPNAME}" SecMain
  SectionIn RO
  
  ; Set output path to the installation directory
  SetOutPath "$INSTDIR"
  
  ; Add files
  File /r "dist\${APPNAME}.exe"
  File /r "assets\*.*"
  File "README.md"
  File "LICENSE"
  File "CHANGELOG.md"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Create start menu shortcuts
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  
  ; Create desktop shortcut if selected
  ${If} $CreateDesktopSC == 1
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe"
  ${EndIf}
  
  ; Write registry keys for Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "UninstallString" '"$INSTDIR\Uninstall.exe" /currentuser'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "DisplayIcon" "$INSTDIR\${APPNAME}.exe,0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "DisplayVersion" "${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "Publisher" "${PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "URLInfoAbout" "${WEBSITE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "HelpLink" "${HELP_URL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "URLUpdateInfo" "${UPDATE_URL}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                 "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "NoRepair" 1
  
  ; Calculate installation size
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" \
                   "EstimatedSize" "$0"
  
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
  ; Remove files
  Delete "$INSTDIR\${APPNAME}.exe"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\CHANGELOG.md"
  
  ; Remove directories
  RMDir /r "$INSTDIR\assets"
  RMDir "$INSTDIR"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APPNAME}"
  Delete "$DESKTOP\${APPNAME}.lnk"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
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
Function .onInit
  ; Initialize variables
  StrCpy $CreateDesktopSC 0
  StrCpy $AssocImages 0
  
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
  
  done:
FunctionEnd

Function LaunchApplication
  ExecShell "" "$INSTDIR\${APPNAME}.exe"
FunctionEnd
