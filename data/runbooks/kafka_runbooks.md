# Kafka On-Call Runbooks

## Runbook: High Consumer Lag
Symptom: Consumer lag on tv.events.playback exceeds 100,000 messages.
Steps:
1. Check consumer group status: kafka-consumer-groups --describe --group tv-playback-consumer
2. Identify slow partitions using lag per partition metrics
3. Scale up consumer instances if lag is growing
4. Check for processing bottlenecks in the consumer application
5. If lag is stable (not growing), monitor for 30 minutes before escalating
Escalate to: Platform team if lag exceeds 500,000 messages

## Runbook: Broker Timeout
Symptom: Consumers reporting broker timeout errors in logs.
Steps:
1. Check broker health in Kafka UI dashboard
2. Verify network connectivity between consumers and brokers
3. Check broker disk usage — alert if >85% full
4. Restart affected broker if unresponsive for >5 minutes
5. Verify consumers resume after broker recovery
Escalate to: Infrastructure team if broker does not recover in 10 minutes

## Runbook: High Error Rate on tv.events.errors
Symptom: Spike in CrashReport or ContentNotFound events.
Steps:
1. Check recent deployments — correlate spike with release time
2. If spike follows a deployment, initiate rollback procedure
3. Check CDN health if ContentNotFound events are spiking
4. Alert mobile/TV app team if CrashReport spike exceeds 500/minute
Escalate to: App team for crash spikes, CDN team for content issues

## Runbook: Missing Device Heartbeats
Symptom: Devices not sending heartbeats to tv.devices.heartbeat for >5 minutes.
Steps:
1. Check device_id in device registry for last known status
2. Verify firmware version — known issue with firmware <2.1.0
3. Check network connectivity for affected devices
4. If >1000 devices affected simultaneously, suspect network outage
Escalate to: Network team if mass outage suspected