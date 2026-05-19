.PHONY: up down build s0 s2 s3 load

up:
	docker compose up --build -d

down:
	docker compose down -v

build:
	docker compose build

s0:
	./scripts/scenarios/s0-normal.sh

s2:
	./scripts/scenarios/s2-payment-delay.sh

s3:
	./scripts/scenarios/s3-network-delay.sh

load:
	k6 run load/k6/checkout.js
