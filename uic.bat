echo off

rem 將子目錄QtApp下的.ui檔案複製到本目錄，並且編譯
copy .\QtApp\MainWindow.ui MainWindow.ui
pyuic5 -o ui_MainWindow.py MainWindow.ui
