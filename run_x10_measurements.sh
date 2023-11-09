for i in $(seq 10); do
  podman stop oracle
  podman rm oracle
  make pod-init
  until [ "$(podman exec oracle lsnrctl status | grep "Service \"xepdb1\"" )" ]; do
      sleep 1
  done
  sleep 10
  echo "db init"
  make pod-init-db
  make pod-run-measurement
done