create-container:
	docker run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol gvenzl/oracle-xe

stop:
	docker stop oracle

start:
	docker start oracle

restart: stop start

import_data:
	tar cf db_generation/volume_data/data.tar db_generation/volume_data/*.sh db_generation/volume_data/*.dmp
	docker volume import vol db_generation/volume_data/data.tar

pod-create-container:
	podman run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol docker.io/gvenzl/oracle-xe

pod-stop:
	podman stop oracle

pod-start:
	podman start oracle

pod-restart: pod-stop pod-start

pod-import_data:
	tar cf db_generation/volume_data/data.tar db_generation/volume_data/*.sh db_generation/volume_data/*.dmp
	podman volume import vol db_generation/volume_data/data.tar
