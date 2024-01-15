docker run --name mariadb \
		--env MARIADB_ROOT_PASSWORD=secret \
		--env MARIADB_USER=user \
		--env MARIADB_PASSWORD=secret \
		--env MARIADB_DATABASE=mydb \
		-d \
		-p 3306:3306 \
		mariadb:11.2.2-jammy

