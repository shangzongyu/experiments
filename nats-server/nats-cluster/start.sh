#!/usr/bin/env bash

nohup nats-server -c ~/code/github-shine/experiments/nats-server/nats-cluster/node1/nats-server.conf -D &
nohup nats-server -c ~/code/github-shine/experiments/nats-server/nats-cluster/node2/nats-server.conf -D &
nohup nats-server -c ~/code/github-shine/experiments/nats-server/nats-cluster/node3/nats-server.conf -D &
