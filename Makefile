run-celery:
	celery -A tasks worker --loglevel=info

run-redis:
	bash redis/run.sh

delete-redis:
	docker rm -f redis-stack
	
clean-output:
	rm -rf output/gfs*