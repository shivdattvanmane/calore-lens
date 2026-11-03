@echo off
title Calorie Lens Web Studio
echo ======================================================
echo    CALORIE LENS: INDIAN FOOD NUTRIENT ESTIMATOR
echo ======================================================
echo.
echo Launching server at http://127.0.0.1:8000/
echo Opening web interface in your default browser...
echo.
start http://127.0.0.1:8000/
python -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
