create-container:
	docker run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol gvenzl/oracle-xe

init: create-container import_data python

stop:
	docker stop oracle

start:
	docker start oracle

restart: stop start

import_data:
	mkdir import
	cp db_generation/create_user.sql db_generation/volume_data/*.py db_generation/volume_data/*.sh db_generation/volume_data/*.sql db_generation/volume_data/*.dmp import/
	cd import
	tar cf data.tar *
	docker volume import vol data.tar
	cd ..
	rm -rf import

python:
	docker exec -u=0 oracle microdnf install python3

connect:
	docker exec --interactive --tty oracle sh

pod-create-container:
	podman run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol docker.io/gvenzl/oracle-xe

pod-init: pod-create-container pod-python pod-import_data

pod-stop:
	podman stop oracle

pod-start:
	podman start oracle

pod-restart: pod-stop pod-start

pod-import_data:
	mkdir import
	cp db_generation/create_user.sql db_generation/drop_tables.sql db_generation/volume_data/*.py db_generation/volume_data/*.sh db_generation/volume_data/*.sql db_generation/volume_data/*.dmp import/
	cd import && \
		tar cf data.tar * && \
		podman volume import vol data.tar
	rm -rf import

pod-connect:
	podman exec --interactive --tty oracle sh

pod-python:
	podman exec -u=0 oracle microdnf install python3
