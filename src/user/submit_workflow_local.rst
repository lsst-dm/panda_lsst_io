.. _submit_workflow_locally:

How to submit a workflow (locally or developer)
===============================================

**Here are instructions how to submit a PanDA workflow to local sites**.

**To submit a workflow remotely, please check** :ref:`submit_workflow_remotely`.

To submit a workflow to PanDA system, here are several general notes:

- **setup environment**. To seupt workflows from USDF, FrDF and UKDF,
  we use the cvmfs to setup the environments. To submit workflows from IDF,
  we can only run remote submission.

- **YAML configuration**. The YAML configuration for BPS submission.

- **butler configuration**. Butler configuration needs to be configured correctly,
  for BPS to generate Quantum Graph correctly.

- **local submission**. For the local submission, BPS will create Quantum Graph
  files locally at first and then submit the workflow to the PanDA system. In
  this case, users need to make sure that the PanDA jobs can access the Quantum
  Graph directory with correct permission.


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


Ping PanDA Service
~~~~~~~~~~~~~~~~~~

After setting up the environment, users can try to ping PanDA service to make sure the settings are ok.

If the BPS_WMS_SERVICE_CLASS is not set, set it through::

   $> export BPS_WMS_SERVICE_CLASS=lsst.ctrl.bps.panda.PanDAService

Ping the PanDA system to check whether the service is ok::

   $> bps ping

**In this step, it will look for tokens for authorization. If you don't have a token or you are not registered yet,
please check** :ref:`user_authentication`.

Prepare YAML configuration
--------------------------

YAML configuration
~~~~~~~~~~~~~~~~~~

As any other Rubin workflow submitted with BPS commands, PanDA based
data processing requires a YAML configuration file. The YAML settings,
common for different BPS plugins provided here::

    https://pipelines.lsst.io/modules/lsst.ctrl.bps/quickstart.html#defining-a-submission

Later in this section we focus on PanDA specific and minimal set of the
common settings supplied in the YAML with *bps submit <config>.yaml*
command. They are::

   -  requestWalltime: 90000 maximum wall time on the execution node allowed to
      run a single job in seconds

   -  NumberOfRetries: 1 number of attempts to successfully execute a job. It is
      recommended to set this parameter at least to 5 due to preemptions
      of machines used in the GKE cluster

   -  whenSaveJobQgraph: "NEVER" this parameter is mandatory because PanDA
      plugin is currently supports only a single quantum graph file
      distribution model

   -  idds_server: "https://aipanda015.cern.ch:443/idds" this is the URL of
      the iDDS server used for the workflow orchestration

   -  sw_image: "spodolsky/centos:7-stack-lsst_distrib-d_2021_08_11"
      defines the Docker image with the SW distribution to use on the
      computation nodes

   -  fileDistributionEndPoint:
      "s3://butler-us-central1-panda-dev/hsc/{payload_folder}/{uniqProcName}/"
      this is bucket name and path to the data used in the workflow

   -  s3_endpoint_url: "https://storage.googleapis.com" the address of the
      object storage server

   -  payload_folder: payload name of the folder where the quantum graph
      file will be stored

   -  runner_command. This is the command will be executed in container by
      the Pilot instance. The ${{IN/L}} expression is the PanDA
      substitution rule to be used during jobs generation.

   -  createQuantumGraph: '${CTRL_MPEXEC_DIR}/bin/pipetask qgraph -d
      "{dataQuery}" -b {butlerConfig} -i {inCollection} -p
      {pipelineYaml} -q {qgraphFile} {pipelineOptions}' this command
      does not contain any PanDA specific parameters and executes at the
      submission node on the local installation

   -  runQuantumCommand: '${CTRL_MPEXEC_DIR}/bin/pipetask --long-log run -b
      {butlerConfig} --output-run {outCollection} --qgraph
      {fileDistributionEndPoint}/{qgraphFile} --qgraph-id {qgraphId}
      --qgraph-node-id {qgraphNodeId} --skip-init-writes --extend-run
      --clobber-outputs --skip-existing' in this command we replace the
      CTRL_MPEXEC_DIR on container_CTRL_MPEXEC_DIR because it will be
      executed on the computation node in container

After implementing lazy variables there is not container release
specific variables in the YAML file.

Site&Memory requirements in YAML files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * Only request memory and let PanDA do the scheduling(do not define *queue*).
    Here is an example::

       computeCloud: "US"
       computeSite: "SLAC"
       requestMemory: 2048

       pipetask:
           pipetaskInit:
               requestMemory: 4000

       executionButler:
           requestMemory: 4000

  * *Clustering* memory requirements: Here is an example to put 4 jobs of pipetasks into
    a *diffim* cluster. In the example, *memoryMultiplier* is used to boost memory when a job
    failed because of running out of memory::

       computeCloud: "US"
       computeSite: "SLAC"
       requestMemory: 2048

       cluster:
           diffim:
               requestMemory: 8000
               memoryMultiplier: 1.5
               numberOfRetries: 3

       executionButler:
           requestMemory: 4000

  * Another example by specifying queues (Here a *queue* is defined)::

       computeCloud: "US"
       computeSite: "SLAC"
       requestMemory: 2048

       pipetask:
           pipetaskInit:
               requestMemory: 4000

           forcedPhotCoadd:
               # *requestMemory is still required here.*
               # *Otherwise it can be schedule to the merge*
               # *queue, but the requestMemory is still 2048*
               requestMemory: 4000
               queue: "SLAC_Rubin_Merge"

  * Another example to get multiple CPU Cores. Currently only the queue *<site>_Rubin_Extra_Himem* supports multi-cores.
    If the job needs multi-cores, the queue must be specified and *requestCpus* is needed. With multi-cores,
    the *requestMemory* is the total memory of all CPU cores::

       computeCloud: "US"
       computeSite: "SLAC"
       requestMemory: 2048

       pipetask:
           pipetaskInit:
               requestCpus: 2
               queue: "SLAC_Rubin_Extra_Himem"
               requestMemory: 8000

           forcedPhotCoadd:
               # *requestMemory is still required here.*
               # *Otherwise it can be schedule to the merge*
               # *queue, but the requestMemory is still 2048*
               requestMemory: 4000
               queue: "SLAC_Rubin_Merge"

Example YAML configuration for local submission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example YAML file for local submission can be found in github or in the LSST stack::
  https://raw.githubusercontent.com/lsst/ctrl_bps_panda/main/python/lsst/ctrl/bps/panda/conf_example/test_usdf.yaml
  $CTRL_BPS_PANDA_DIR/python/lsst/ctrl/bps/panda/conf_example/test_usdf.yaml

Here is an example for local submission::

    LSST_VERSION: w_2024_14

    includeConfigs:
      - ${CTRL_BPS_PANDA_DIR}/config/bps_usdf.yaml
      # - ${CTRL_BPS_PANDA_DIR}/config/bps_frdf.yaml  # To submit workflows to FrDF
      # - ${CTRL_BPS_PANDA_DIR}/config/bps_ukdf.yaml  # To submit workflows to UKDF

    pipelineYaml: "${DRP_PIPE_DIR}/pipelines/LSSTCam-imSim/DRP-test-med-1.yaml#isr"
    # pipelineYaml: "${DRP_PIPE_DIR}/pipelines/LSSTCam-imSim/DRP-test-med-1.yaml#step1"

    computeSite: SLAC
    requestMemory: 4000
    memoryMultiplier: 1.2

    payload:
      payloadName: test_DF_{computeSite}
      inCollection: "2.2i/defaults"
      # dataQuery: "instrument='LSSTCam-imSim' and skymap='DC2' and exposure in (214433) and detector=10"
      dataQuery: "instrument='LSSTCam-imSim' and skymap='DC2' and exposure in (214433)"
      # butlerConfig: panda-test-med-1        # butler configuration for FrDF and UKDF
      butlerConfig: /repo/dc2                 # butler configuration for USDF

Butler configuration
--------------------

Make sure you have db-auth.yaml in your $HOME area. The content of it is
something like: ::

   $> cat ${HOME}/.lsst/db-auth.yaml
   - url: postgresql://usdf-butler.slac.stanford.edu:5432/lsstdb1
   username: rubin
   password: *********************************************************


Submit a workflow
-----------------

Local submission
~~~~~~~~~~~~~~~~

For the first time PanDA uses the higher-level butler directories (e.g., first PanDA run for u/<your_operator_name>). If permissions are not set right, the pipetaskInit job will die with a ``Failed to execute payload:[Errno 13] Permission denied: '/sdf/group/rubin/repo/main/<output collection>'`` message.
Note: one cannot pre-test permissions by manually running pipetask as the PanDA job is executed as a special user.
In this case, you need to grant group permission for PanDA to access the butler directory.::

   $> chmod -R g+rws /sdf/group/rubin/repo/main/u/<your_operator_name>

Here is the command to submit a local workflow::

    bps submit test_local.yaml

Submit a workflow (Developers)
------------------------------

Developers may have private lsst stack environment. Here are instructions for developers.

Copy the stack environment setup script from cvmfs to your local directory and update the lsst setup part to your private repo: ::

   $> latest=$(ls -td /cvmfs/sw.lsst.eu/linux-x86_64/panda_env/v* | head -1)
   $> cp $latest/setup_lsst.sh /local/directory/
   $> <update /local/directory/setup_lsst.sh>
   $> source /local/directory/setup_lsst.sh
   $> source $latest/setup_panda_usdf.sh (or setup_panda_cern.sh if using PanDA at CERN)

``Note``: Make sure PanDA can read your private repo: ::

   $> chmod -R g+rxs <your private development repo>

Here is an example for local submission for developer, with customizing ``setupLSSTEnv`` to point to your private development repo: ::

    LSST_VERSION: w_2024_14

    includeConfigs:
      - ${CTRL_BPS_PANDA_DIR}/config/bps_usdf.yaml
      # - ${CTRL_BPS_PANDA_DIR}/config/bps_frdf.yaml  # To submit workflows to FrDF
      # - ${CTRL_BPS_PANDA_DIR}/config/bps_ukdf.yaml  # To submit workflows to UKDF

    pipelineYaml: "${DRP_PIPE_DIR}/pipelines/LSSTCam-imSim/DRP-test-med-1.yaml#isr"
    # pipelineYaml: "${DRP_PIPE_DIR}/pipelines/LSSTCam-imSim/DRP-test-med-1.yaml#step1"

    computeSite: SLAC
    requestMemory: 4000
    memoryMultiplier: 1.2

    payload:
      payloadName: test_DF_{computeSite}
      inCollection: "2.2i/defaults"
      # dataQuery: "instrument='LSSTCam-imSim' and skymap='DC2' and exposure in (214433) and detector=10"
      dataQuery: "instrument='LSSTCam-imSim' and skymap='DC2' and exposure in (214433)"
      # butlerConfig: panda-test-med-1        # butler configuration for FrDF and UKDF
      butlerConfig: /repo/dc2                 # butler configuration for USDF

    # setup private repo
    setupLSSTEnv: >
      source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/{LSST_VERSION}/loadLSST.bash;
      pwd; ls -al;
      setup lsst_distrib;
      setup -k -r /path/to/your/test/package;
