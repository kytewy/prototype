.PHONY: dev test-back test-front debug-back debug-front clean

# Build and start both frontend and backend (detached)
dev:
	docker-compose up --build -d

# Run backend tests inside backend container
test-back:
	docker-compose exec backend pytest

# Run frontend tests inside frontend container
test-front:
	docker-compose exec frontend pnpm test

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

# Stop and remove containers, networks, volumes, and orphans
clean:
	docker-compose down --volumes --remove-orphans

nuke:
	docker-compose down
	docker system prune -f
	docker-compose build --no-cache frontend
	docker-compose up -d
	docker-compose exec frontend npm test