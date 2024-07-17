Dev: PanDA @ USDF
=================

**Here are instructions only for developers to deploy PanDA @ USDF**.

The PanDA k8s deployment includes these components below. The PanDA system is deployed to USDF k8s cluster
through ``helm``. In this chapter, the details about how to deploy the PanDA dev system at USDF are described.

- **PanDA**. PanDA server, JEDI and postgres database.
- **iDDS**. The iDDS (restful service and daemon agents are in one pod) and postgres database.
- **Harvester**. Harvester and mariadb.
- **PanDA monitor**. The monitor.
- **Indigo IAM**. The IAM to manage OIDC user registration and user accounts. Optional.
- **ActiveMQ**. The messaging service.


.. image:: ../_images/panda_k8s_usdf.png
 :width: 5.30895in
 :height: 4.46667in


Setup
-----
Setup environment to access the ``usdf-panda--dev`` k8s cluster.

- Get the tokens to authenticate usdf-panda--dev cluster https://k8s.slac.stanford.edu/usdf-panda-dev. Login to it to get tokens

- Follow the instructions to setup the environments in a USDF bash environment, such as ``rubin-dev``.

Deploy secrets
--------------
Currently the secrets are in ``BitBucket`` private git repo, please contact the PanDA team to get the secrets.

Instructions to deploy the secrets::

    helm install/upgrade panda-secrets -n panda secrets/  -f secrets/values.yaml -f secrets/values-secret.yaml
    helm install/upgrade panda-secrets -n mariadb secrets/  -f secrets/values.yaml -f secrets/values-secret.yaml


Main deployment
---------------
Checkout the main deployment scripts::

    git clone https://github.com/PanDAWMS/panda-k8s.git
    cd panda-k8s

Mariadb deployment::

    kubectl create namespace mariadb
    helm repo add mariadb-operator https://mariadb-operator.github.io/mariadb-operator
    helm install -n mariadb mariadb-operator mariadb-operator/mariadb-operator

    # iam-db
    helm install -n mariadb iam-db-dev helm/mariadb/iam-db/ -f helm/mariadb/iam-db/values.yaml  -f helm/mariadb/iam-db/values/values-lsst.yaml

    # harvester-db: multiple instances
    helm install -n mariadb harvester-db-dev-0 helm/mariadb/harvester-db/ -f helm/mariadb/harvester-db/values.yaml  -f helm/mariadb/harvester-db/values/values-lsst.yaml
    helm install  -n mariadb harvester-db-dev-1 helm/mariadb/harvester-db/ -f helm/mariadb/harvester-db/values.yaml  -f helm/mariadb/harvester-db/values/values-lsst.yaml

Services deployment::

    # helm install -n panda iam-dev helm/iam/ -f helm/iam/values.yaml -f helm/iam/values/values-lsst.yaml
    helm install -n panda msgsvc-dev helm/msgsvc/ -f helm/msgsvc/values.yaml -f helm/msgsvc/values/values-lsst.yaml
    helm install -n panda panda-dev helm/panda/ -f helm/panda/values.yaml -f helm/panda/values/values-lsst.yaml
    helm install -n panda idds-dev helm/idds/ -f helm/idds/values.yaml -f helm/idds/values/values-lsst.yaml
    helm install -n panda harvester-dev helm/harvester/ -f helm/harvester/values.yaml -f helm/harvester/values/values-lsst.yaml
    helm install -n panda bigmon-dev helm/bigmon/ -f helm/bigmon/values.yaml -f helm/bigmon/values/values-lsst.yaml
