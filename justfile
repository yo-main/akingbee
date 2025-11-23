api:
    go run .

test-migration:
    mv akingbee.db akingbee.local.db
    scp -i ~/workspace/homelab/infra/ansible/secrets/id_rsa ansible@akingbee.com:/apps/akingbee/akingbee.db akingbee.db
    go run . api

