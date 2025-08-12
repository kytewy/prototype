.PHONY: dev dev-front dev-back test test-back test-front debug debug-back debug-front clean nuke logs logs-front logs-back restart restart-front restart-back

#######################
# Development Commands #
#######################

# Build and start both frontend and backend (detached)
dev:
	docker-compose up --build -d

# Build and start only frontend (detached)
dev-front:
	docker-compose up --build -d frontend

# Build and start only backend (detached)
dev-back:
	docker-compose up --build -d backend

##################
# Test Commands #
##################

# Run all tests
test: test-back test-front

# Run backend tests inside backend container
test-back:
	docker-compose exec backend pytest -v

# Run frontend tests inside frontend container
test-front:
	docker-compose exec frontend pnpm test -v

###################
# Debug Commands #
###################

# Clean, rebuild both services and run all tests
debug: debug-back debug-front

# Clean, rebuild backend and run backend tests
debug-back:
	make clean
	docker-compose build backend
	docker-compose up -d backend
	make test-back

# Clean, rebuild frontend and run frontend tests
debug-front:
	make clean
	docker-compose build frontend
	docker-compose up -d frontend
	make test-front

####################
# Utility Commands #
####################

# View logs for all services
logs:
	docker-compose logs -f

# View logs for frontend service
logs-front:
	docker-compose logs -f frontend

# View logs for backend service
logs-back:
	docker-compose logs -f backend

# Restart all services
restart:
	docker-compose restart

# Restart frontend service
restart-front:
	docker-compose restart frontend

# Restart backend service
restart-back:
	docker-compose restart backend

# Stop and remove containers, networks, volumes, and orphans
clean:
	docker-compose down --volumes --remove-orphans

# Complete rebuild of frontend container and run tests
nuke:
	docker-compose down
	docker system prune -f
	docker-compose build --no-cache frontend
	docker-compose up -d
	docker-compose exec frontend pnpm test

nuke-back:
	docker-compose down
	docker system prune -f
	docker-compose build --no-cache backend
	docker-compose up -d
	docker-compose exec backend pytest -v