Start-Process "ollama" -ArgumentList "serve"

Start-Sleep -Seconds 5

cd backend
uvicorn app:app --reload
