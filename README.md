# Flask running on OpenShift that routes alertmanager alerts to HP OMi
  
Prometheus Alertmanager - sends Prometheus alerts to HP OMi (Operation Manager i)  

Settings.ini setting as post-url, assignee group and OpenShift Version (3 or 4)

template.xml is needed for converting json to omi xml output

## Installing alert2omi

### Building the application
In the project where you want to deploy the application, run the following
commands to build from the provided Openshift template:
```
oc delete all -l app=alert2omi
oc process -f build.yml | oc create -f-
```

### Deploying the application
After a successful build, run the following commands in the same project to
deploy the built image using the provided Openshift template:
```
oc process -f deploy.yml | oc create -f-
```

## Configuring Alertmanager
changes needed for alertmanager:

```
- name: alert2omi
  webhook_configs:
  - send_resolved: false
    url: http://alert2omi.prometheus.svc:8080/webhook
```

Tested on OpenShift 3.6 - 3.7 and 4.1 - 4.3
