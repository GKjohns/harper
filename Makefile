# Define the commands to use for Python, MongoDB via Homebrew, and opening a web page
PYTHON := python
MONGODB_START := brew services start mongodb-community@7.0
MONGODB_STOP := brew services stop mongodb-community@7.0
OPEN := open
LSOF := lsof -i :5000
TMUX := tmux

# Define the paths to your server and frontend files
SERVER_SCRIPT := backend/server/server.py
FRONTEND_INDEX := frontend/index.html
TMUX_SESSION_NAME := harper_server

# Default target to start the backend, frontend, and database
all: start-db start-backend start-frontend

# Target to start the MongoDB database using Homebrew
start-db:
	@echo "Starting MongoDB database with Homebrew..."
	@$(MONGODB_START)

# Target to start the Flask server in a new tmux session
start-backend:
	@echo "Starting Flask server in a tmux session..."
	@$(TMUX) new-session -d -s $(TMUX_SESSION_NAME) "$(PYTHON) $(SERVER_SCRIPT); read"

# Target to open the frontend webpage
start-frontend:
	@echo "Opening the frontend website..."
	@$(OPEN) $(FRONTEND_INDEX)

# Target to stop the Flask server
stop-backend:
	@if $(TMUX) has-session -t $(TMUX_SESSION_NAME) 2>/dev/null; then \
		echo "Killing tmux session $(TMUX_SESSION_NAME)..."; \
		$(TMUX) kill-session -t $(TMUX_SESSION_NAME); \
		echo "Tmux session $(TMUX_SESSION_NAME) killed."; \
	else \
		echo "Tmux session $(TMUX_SESSION_NAME) not found."; \
	fi

# Clean command to stop the MongoDB server and Flask server
clean:
	@echo "Cleaning up..."
	@make stop-backend
	@echo "Stopping MongoDB database..."
	@$(MONGODB_STOP)
	@echo "Clean up operations completed."
