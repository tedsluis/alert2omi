# Flask running on OpenShift that routes alertmanager alerts to HP OMi
  
Prometheus Alertmanager - sends Prometheus alerts to HP OMi (Operation Manager i)  

Settings.ini setting as post-url, assignee group

template.xml is needed for converting json to omi xml output

installing alert2omi:

oc delete all -l app=alert2omi -n prometheus
oc create -f alert2omi.yml -n prometheus

changes needed for alertmanager:

```
- name: alert2omi
  webhook_configs:
  - send_resolved: false
    url: http://alert2omi.prometheus.svc:8080/webhook
```

Tested on OpenShift 3.6 - 3.7
