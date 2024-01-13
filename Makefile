# Makefile

# Define the commands to use for Python and opening a web page
PYTHON := python
OPEN := open

# Define the paths to your server and frontend files
SERVER_SCRIPT := backend/server/server.py
FRONTEND_INDEX := frontend/index.html

# Default target to start both the backend and frontend
all: start-frontend start-backend 

# Target to start the Flask server
start-backend:
	@echo "Starting Flask server..."
	@$(PYTHON) $(SERVER_SCRIPT)

# Target to open the frontend webpage
start-frontend:
	@echo "Opening the frontend website..."
	@$(OPEN) $(FRONTEND_INDEX)

# Add a clean command if needed
clean:
	@echo "Clean up operations here (if any)"
