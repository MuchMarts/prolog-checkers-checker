build:
	docker build -t checkers-prolog-app .

run:
	docker run --rm -it checkers-prolog-app --mode run

test:
	docker run --rm -it checkers-prolog-app --mode test

rerun:
	make build && make run

retest:
	make build && make test