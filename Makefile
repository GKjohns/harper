# Define the commands to use for Python, MongoDB via Homebrew, and opening a web page
PYTHON := python
MONGODB_START := brew services start mongodb-community@7.0
MONGODB_STOP := brew services stop mongodb-community@7.0
OPEN := open

# Define the paths to your server and frontend files
SERVER_SCRIPT := backend/server/server.py
FRONTEND_INDEX := frontend/index.html

# Default target to start the backend, frontend, and database
all: start-db start-backend start-frontend

# Target to start the MongoDB database using Homebrew
start-db:
	@echo "Starting MongoDB database with Homebrew..."
	@$(MONGODB_START)

# Target to stop the MongoDB database using Homebrew
stop-db:
	@echo "Stopping MongoDB database with Homebrew..."
	@$(MONGODB_STOP)

# Target to start the Flask server
start-backend:
	@echo "Starting Flask server..."
	@$(PYTHON) $(SERVER_SCRIPT)

# Target to open the frontend webpage
start-frontend:
	@echo "Opening the frontend website..."
	@$(OPEN) $(FRONTEND_INDEX)

# Clean command to stop the MongoDB server
clean:
	@echo "Stopping MongoDB database..."
	@$(MONGODB_STOP)
