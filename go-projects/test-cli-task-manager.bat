@echo off
cd go-projects/cli-task-manager
echo Testing CLI Task Manager...
echo.
echo Running basic functionality test...
echo 1 > input.txt
echo 6 >> input.txt
go run main.go < input.txt
del input.txt
echo.
echo Test completed.
pause
