build:
	docker build -t checkers-prolog-app .

run:
	docker run --rm -it checkers-prolog-app

rerun:
	make build && make run