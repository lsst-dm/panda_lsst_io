Management instructions
=======================

Show services and pods::

    # kubectl get all -n panda
    NAME                                      READY   STATUS    RESTARTS   AGE
    pod/bigmon-dev-main-0                     1/1     Running   0          6d21h
    pod/bigmon-dev-main-1                     1/1     Running   0          6d21h
    pod/idds-dev-rest-0                       1/1     Running   0          4d2h
    pod/idds-dev-rest-1                       1/1     Running   0          4d2h
    pod/msgsvc-dev-activemq-7c47bb7d7-97nd6   1/1     Running   0          20d
    pod/panda-dev-jedi-0                      1/1     Running   0          4h19m
    pod/panda-dev-jedi-1                      1/1     Running   0          4h20m
    pod/panda-dev-server-0                    1/1     Running   0          4h19m
    pod/panda-dev-server-1                    1/1     Running   0          4h20m

    NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)             AGE
    service/bigmon-dev-main       ClusterIP   10.98.243.181    <none>        443/TCP             6d21h
    service/idds-dev-rest         ClusterIP   10.108.12.12     <none>        8443/TCP,8080/TCP   4d2h
    service/msgsvc-dev-activemq   ClusterIP   10.103.208.12    <none>        61613/TCP           110d
    service/panda-dev-jedi        ClusterIP   10.104.113.232   <none>        80/TCP,443/TCP      4d17h
    service/panda-dev-server      ClusterIP   10.96.29.71      <none>        80/TCP,443/TCP      4d17h

    NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/msgsvc-dev-activemq   1/1     1            1           110d

    NAME                                            DESIRED   CURRENT   READY   AGE
    replicaset.apps/msgsvc-dev-activemq-7c47bb7d7   1         1         1       110d

    NAME                                READY   AGE
    statefulset.apps/bigmon-dev-main    2/2     6d21h
    statefulset.apps/idds-dev-rest      2/2     4d2h
    statefulset.apps/panda-dev-jedi     2/2     4d17h
    statefulset.apps/panda-dev-server   2/2     4d17h

Show secrets::

    # kubectl get secrets -n panda

Show ingress::

    # kubectl get ingress -n panda

    NAME               CLASS    HOSTS                                      ADDRESS   PORTS     AGE
    bigmon-dev-main    <none>   rubin-panda-bigmon-dev.slac.stanford.edu             80, 443   6d21h
    idds-dev-rest      <none>   rubin-panda-idds-dev.slac.stanford.edu               80, 443   4d2h
    panda-dev-server   <none>   rubin-panda-server-dev.slac.stanford.edu             80, 443   4d17h

Describe pod details::

    kubectl describe <k8s service type: pod, service, ingress, secret and so on> <podname> -n panda
    Eg: kubectl describe pod bigmon-dev-main-0 -n panda
    Eg: kubectl describe statefulset bigmon-dev-main -n panda

    Eg: kubectl describe statefulset bigmon-dev-main -n panda

Login to pods::

    kubectl exec -n panda -it <podname> -- bash
    Eg: kubectl exec -n panda -it bigmon-dev-main-0 -- bash

Pod logs::

    Normally the pod logs are under /var/log/panda, /var/log/idds.
    To understand what the pod is running, you can ‘ps -ef’ or ‘ps -ef|grep sh’ to list all processes. The first process will tell you what the pod is doing.

Harvester debug::

    kubectl exec -n panda -it harvester-dev-0 -- bash
    # Check condor
    source  /data/condor/condor/condor.sh
    Condor_q
    # Check harvester logs, for example:
    grep 'workers status' /var/log/panda/panda-submitter.log
    # Start httpd if it’s not running: harvester httpd is used to export harvester logs
    runuser -u atlpan -g zp -- /sbin/httpd
    # stop/start harvester services
    runuser -u atlpan -g zp -- /opt/harvester/etc/rc.d/init.d/panda_harvester-uwsgi stop
    runuser -u atlpan -g zp -- /opt/harvester/etc/rc.d/init.d/panda_harvester-uwsgi start

Panda server debug::

    kubectl exec -n panda -it panda-dev-server-0 -- bash
    # start/stop panda server (it has http web services and master.py daemons)
    runuser -u atlpan -g zp -- /etc/rc.d/init.d/httpd-pandasrv stop
    runuser -u atlpan -g zp -- /etc/rc.d/init.d/httpd-pandasrv start

    # Http server logs
    tail -f /var/log/panda/panda_server_error_log
    ls /var/log/panda/panda-JobDispatcher.log
    ls /var/log/panda/panda-UserIF.log

    # Daemon logs
    tail -f /var/log/panda/panda_daemon_stdout.log
    ls /var/log/panda/*.log
    ls /var/log/panda/panda-DBProxy.log

Panda jedi debug::

    kubectl exec -n panda -it panda-dev-jedi-0 -- bash
    # start/stop panda jedi
    runuser -u atlpan -g zp -- /etc/rc.d/init.d/panda-jedi stop
    runuser -u atlpan -g zp -- /etc/rc.d/init.d/panda-jedi start

    # Logs
    ls /var/log/panda/

iDDS debug::

    kubectl exec -n panda -it idds-dev-rest-0 -- bash
    # status/start/stop services
    supervisorctl status
    supervisorctl start <servicename|all>
    supervisorctl stop <servicename|all>

    # Check logs
    ll /var/log/idds/

