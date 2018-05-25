oc delete all -l app=alert2omi -n prometheus
oc project prometheus
oc create -f alert2omi.yml
