.. _run_prun:

What is prun
============

prun is a PanDA client CLI, which can be used to send user scripts to be executed at remote sites.

To use prun to run jobs at remote sites, here are several general notes:

- **source codes uploading**. prun will automatically upload source codes in the current directory
  to PanDA cache, which is a http service to ship user codes to remote sites. It has some limitation
  on the file size. Before using prun, it's good to make sure the current directory (and subdirectory)
  is not too big. And don't put sensitive information such as passwords in the current directory.
  Maybe it's good to create a new directory for it.

- **remote execution**. The source codes in the current directory will be shipped to the execution node
  and put in the working directory. It doesn't clone the environment to the execution node. So users
  need to setup the environment by themselves.

Setup environment
-----------------

Setup environment with CVMFS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The submit workflows from USDF, FrDF and UKDF, the CVMFS is available. Users can use
CVMFS to setup the environments::

  latest=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
  source $latest/setup_lsst.sh <lsst stack version>
  # source $latest/setup_lsst.sh w_2024_14   # for example
  source $latest/setup_panda.sh

For LSST stack verion older than w_2024_14, this line below is required for remote submission::

  source $latest/setup_bps.sh

Setup environment on IDF
~~~~~~~~~~~~~~~~~~~~~~~~

The Rubin Science Platform (RSP) can be accessed from the JupyterLab
notebook configured for the IDF at: ::

    https://data-int.lsst.cloud/

Choose "Notebooks" and authorize lsst-sqre with your user credentials.
After successful authentication, choose a cached image or the latest weekly
version (recommended) from the drop down menu.

.. image:: ../_images/JupyterLab.png
   :width: 6.5in
   :height: 2.66667in

Open a terminal (menu **File > New > Terminal**).

On IDF, CVMFS is not available. However, on IDF, normal environments should already be setup.
Users only need to run this command below after login to data-int.lsst.cloud or data.lsst.cloud. ::

    setup lsst_distrib

**IDF can only run remote submission currently, to submit workflows to USDF, FrDF or UKDF.**

Ping PanDA Service
~~~~~~~~~~~~~~~~~~

After setting up the environment, users can try to ping PanDA service to make sure the settings are ok.

If the BPS_WMS_SERVICE_CLASS is not set, set it through::

   $> export BPS_WMS_SERVICE_CLASS=lsst.ctrl.bps.panda.PanDAService

Ping the PanDA system to check whether the service is ok::

   $> bps ping

**In this step, it will look for tokens for authorization. If you don't have a token or you are not registered yet,
please check** :ref:`user_authentication`.

Prepare script
--------------------------

Here is a simple example::

  >>cat my_test_command.sh
  #!/bin/bash

  latest=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)

  source $latest/setup_lsst.sh w_2024_14

  # LSST_LOCAL_PROLOG will run at the beginning to setup some pilot env
  echo $LSST_LOCAL_PROLOG
  source $LSST_LOCAL_PROLOG

  # show butler information
  env|grep DAF_BUTLER_REPOSITORY_INDEX
  cat $DAF_BUTLER_REPOSITORY_INDEX

  # other user commands

How to submit jobs to remote sites::

  prun --noBuild --workingGroup Rubin --vo wlcg --prodSourceLabel test  --site SLAC_Rubin --exec "pwd; ls; chmod +x my_test_command.sh; ./my_test_command.sh" --outDS user.wguan.`uuidgen` --nJobs 1
  prun --noBuild --workingGroup Rubin --vo wlcg --prodSourceLabel test --site LANCS_Rubin --exec "pwd; ls; chmod +x my_test_command.sh; ./my_test_command.sh" --outDS user.wguan.`uuidgen` --nJobs 1
  prun --noBuild --workingGroup Rubin --vo wlcg --prodSourceLabel test --site CC-IN2P3_Rubin --exec "pwd; ls; chmod +x my_test_command.sh; ./my_test_command.sh" --outDS user.wguan.`uuidgen` --nJobs 1

Monitor jobs
~~~~~~~~~~~~~

The prun command submits tasks to PanDA systme. They are not workflows.
These tasks can only be found from the task view::

    https://usdf-panda-bigmon.slac.stanford.edu:8443/tasks/?display_limit=300
