create-container:
	docker run -d -p 1521:1521 -e ORACLE_PASSWORD=test --name oracle -v vol:/vol gvenzl/oracle-xe

init: create-container import-data

stop:
	docker stop oracle

start:
	docker start oracle

restart: stop start

#doesn't work in powershell
import-data:
	mkdir import
	cp db_generation/create_user.sql db_generation/drop_tables.sql import/
	cp volume_data/*.sh volume_data/*.sql volume_data/*.dmp import/
	cp queries/* import/
	docker cp import/. oracle:/vol
	rm -rf import
	docker exec -u=0 oracle chown -R oracle /vol/

connect:
	docker exec --interactive --tty oracle bash

run-measurement:
	docker exec oracle sh /vol/time.sh

run-measurement-10:
	docker exec oracle sh /vol/run_measurements_docker.sh

take-average:
	docker exec oracle cat /vol/clear_res.txt | py average.py

init-db:
	docker exec oracle sh /vol/init.sh

restore:
	docker exec oracle sh /vol/restore.sh

drop-container: stop
	docker rm oracle

run-raport:
	docker exec oracle sh /vol/raport.sh

print-raport:
	docker exec oracle cat /vol/res.txt | python3 raport.py

print-raport-py:
	docker exec oracle cat /vol/res.txt | py raport.py

raport: run-raport print-raport