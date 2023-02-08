Site Environments
=================

The site environments required for running PanDA jobs.

Export LSST_LOCAL_PROLOG
------------------------

For running PanDA jobs, the site only needs to export LSST_LOCAL_PROLOG.
When LSST_LOCAL_PROLOG is defined, lsst pilot wrapper will source
LSST_LOCAL_PROLOG during running. In this way, it will not affect other experiments.
LSST_LOCAL_PROLOG can be defined in .bashrc. for example::

  export LSST_LOCAL_PROLOG=/sdf/home/l/lsstsvc1/.lsst/local_prolog.sh

The content of LSST_LOCAL_PROLOG
--------------------------------

Here are the content of LSST_LOCAL_PROLOG and corresponding descriptions.

- Timezone:

  To set the timezone, it's good for logging format for jobs from different sites::
  export TZ=UTC

- Realtime logging:

  Environments required for realtime logging::
  # set USE_REALTIME_LOGGING to no if no realtime logging.
  export REALTIME_LOGGING_SERVER=google-cloud-logging
  export REALTIME_LOGNAME=Panda-RubinLog
  export REALTIME_LOGFILES=payload-log.json
  export USE_REALTIME_LOGGING=yes

- voms and x509 certificates:

  Setup voms-proxy-info and x509 CA certificates (/etc/grid-security/certificates by default).
  Setup osg for SLAC here (or setup lcg clients here for other sites).
  For EU sites, some lcg libraries are already installed locally. So this line can be ignored::
    # source /cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/current/el8-x86_64/setup.sh

- group permission for new directories:

  It’s used for setting the permissions of some sub-directories in the job::
  umask 007

- lsst accounts:

  Accounts to access google realtime logging service, required by pilots to send realtime logs::
    export GOOGLE_APPLICATION_CREDENTIALS=/sdf/home/l/lsstsvc1/.lsst/gcs-access.json

  Butler db accounts::
    export LSST_DB_AUTH=/sdf/home/l/lsstsvc1/.lsst/db-auth.yaml

  Account to access SLAC objectstore, it’s not required for other sites if there are no objectstores::
    # export AWS_SHARED_CREDENTIALS_FILE=/sdf/home/l/lsstsvc1/.lsst/aws-credentials.ini

- temp directory:

  SLAC temp directory, it’s not required for other sites if the default /tmp works ok
  (The default /tmp directory should be big enough because PanDA and butler will put
  some temp files in the /tmp directory. It’s good to make sure that 2~4 GB per CPU cores)::
    export TMPDIR=/lscratch/lsstsvc1/pilot_temp/
    mkdir -p $TMPDIR

- butler configuration:

  The location of the butler configuration files.
  It can be a posix file or s3 objectstore file::
    # export DAF_BUTLER_REPOSITORY_INDEX="s3://butler-us-central1-panda-dev/dc2/butler-external.yaml"
    # export RUBIN_RUN_TEMP_SPACE="s3://butler-us-central1-panda-dev/"
    export DAF_BUTLER_REPOSITORY_INDEX="/sdf/group/rubin/shared/data-repos.yaml"

- LSST_RUN_TEMP_SPACE:

  A temporary directory to store qgraph files, the execution butler and a few other scripts.
  During 'bps submit', the qgraph files, the execution butler (a sqlite file) and a few other
  scripts will be created and stored in this directory. These files will be accessed by pipeline jobs.
  It should be a share directory or a Grid/Cloud directory which can be accessed by all worker nodes::
    export LSST_RUN_TEMP_SPACE="file:///sdf/group/rubin/sandbox/"


Example LSST_LOCAL_PROLOG
--------------------------------

Here is an example of LSST_LOCAL_PROLOG. It's the configuration for USDF::

  # A copy of /sdf/home/l/lsstsvc1/.lsst/local_prolog.sh
  # It will be called automatically by pilot wrapper.

  # set timezone, good for logging format for jobs from different sites, which will be helpful for debugging.
  export TZ=UTC

  # realtime logging
  # set USE_REALTIME_LOGGING to no if no realtime logging.
  export REALTIME_LOGGING_SERVER=google-cloud-logging
  export REALTIME_LOGNAME=Panda-RubinLog
  export REALTIME_LOGFILES=payload-log.json
  export USE_REALTIME_LOGGING=yes

  # setup voms-proxy-info and x509 CA certificates (/etc/grid-security/certificates by default)
  # setup osg for SLAC here (or setup lcg clients here for other sites)
  # For EU sites, some lcg libraries are already installed locally. So this line can be ignored.
  source /cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/current/el8-x86_64/setup.sh

  # group permission for new directories
  # it’s used for setting the permissions of some sub-directories in the job.
  umask 007

  # lsst accounts
  # accounts to access google realtime logging service, required by pilots to send realtime logs.
  export GOOGLE_APPLICATION_CREDENTIALS=/sdf/home/l/lsstsvc1/.lsst/gcs-access.json

  # butler db accounts
  export LSST_DB_AUTH=/sdf/home/l/lsstsvc1/.lsst/db-auth.yaml

  # account to access SLAC objectstore, it’s not required for other sites if there are no objectstores.
  export AWS_SHARED_CREDENTIALS_FILE=/sdf/home/l/lsstsvc1/.lsst/aws-credentials.ini

  # SLAC temp directory, it’s not required for other sites if the default /tmp works ok
  # (The default /tmp directory should be big enough because PanDA and butler will put
  # some temp files in the /tmp directory. It’s good to make sure that 2~4 GB per CPU cores).
  export TMPDIR=/lscratch/lsstsvc1/pilot_temp/
  mkdir -p $TMPDIR

  # set butlerConfig and fileDistributionEndpoint
  # export DAF_BUTLER_REPOSITORY_INDEX="s3://butler-us-central1-panda-dev/dc2/butler-external.yaml"
  export DAF_BUTLER_REPOSITORY_INDEX="/sdf/group/rubin/shared/data-repos.yaml"

  # A temporary directory to store qgraph files, the execution butler and a few other scripts.
  # During `bps submit`, the qgraph files, the execution butler (a sqlite file) and a few other
  # scripts will be created and stored in this directory. These files will be accessed by pipeline
  # jobs. It should be a share directory.
  # export RUBIN_RUN_TEMP_SPACE="s3://butler-us-central1-panda-dev/"
  export LSST_RUN_TEMP_SPACE="file:///sdf/group/rubin/sandbox/"

