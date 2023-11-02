create-container:
	docker run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol gvenzl/oracle-xe

init: create-container import_data

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

run-measurement:
	docker exec oracle sh /vol/time.sh

take-average:  python
	docker exec oracle python3 /vol/average.py

init-db:
	docker exec oracle sh /vol/init.sh

restore:
	docker exec oracle sh /vol/restore.sh

drop-container: stop
	docker rm oracle

pod-create-container:
	podman run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol docker.io/gvenzl/oracle-xe

pod-init: pod-create-container pod-import_data

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

pod-run-measurement:
	podman exec oracle sh /vol/time.sh

pod-take-average:  pod-python
	podman exec oracle python3 /vol/average.py

pod-init-db:
	podman exec oracle sh /vol/init.sh

pod-restore:
	podman exec oracle sh /vol/restore.sh

pod-drop-container: pod-stop
	podman rm oracle
