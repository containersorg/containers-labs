#!/bin/env bash
# Author: Juan Medina
# Date: 2026-09-12
# Version: 1.0.0
# Description: This script assigns ports to each student account
# for the containers labs. It is meant to be run once per student account.
set -euo pipefail

CONFIG="${HOME}/.containers-labs.env"

if [[ -f "${CONFIG}" ]]; then
  echo "Ports already assigned in ${CONFIG}"
  source ${CONFIG}
  exit 0
fi

OFFSET=$(( (${UID} - 1000) * 5 ))

cat > "$CONFIG" <<EOF
# Ports required for the labs
OFFSET=${OFFSET}
MONO_PORT=$((5000 + ${OFFSET}))
INVENTORY_PORT=$((5001 + ${OFFSET}))
ORDER_PORT=$((5002 + ${OFFSET}))
CUSTOMER_PORT=$((5003 + ${OFFSET}))
BILLING_PORT=$((5004 + ${OFFSET}))

# Ports required for the node ports in the kubernetes labs (lab-13)
# NODE_ORDER_PORT=$((30002 + ${OFFSET}))

# For host-network labs (lab-08 and earlier inter-service calls)
INVENTORY_API_URL="http://127.0.0.1:\${INVENTORY_PORT}"

# For bridge network labs (lab-09 and later inter-service calls)
INVENTORY_API_URL_BRIDGE="http://inventory_service:\${INVENTORY_PORT}"
EOF

# Verify if ~./bashrc already has the source command for the containers-labs.env file
if ! grep -q "source ~/.containers-labs.env" ~/.bashrc; then
  echo "
  set -a
  source ~/.containers-labs.env
  lab-ports() { echo "Your ports: monolithic='$MONO_PORT' inventory='$INVENTORY_PORT' order='$ORDER_PORT' customer='$CUSTOMER_PORT' billing='$BILLING_PORT'"; }
  set +a
  " >> ~/.bashrc
fi

source ${CONFIG}
