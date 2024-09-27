Pilot Environment on CVMFS
==========================

To make sure pilot can run with all required environments, we maintained a pilot environment to
deploy necessary packages to cvmfs.

Contents in Pilot Environment
-----------------------------

Here are the main contents in pilot environment:

- Conda environment with necessary packages.

- Pilot wrapper.

- Pilot.

- Pilot configuration file and Rucio configuration file (for Rucio integration).

- [optional] BPS deployment

- Setup files for users to setup PanDA environment. Users can run the setup files to setup LSST
  stack and PanDA environment, in order to submit jobs to PanDA.

How to manage it
----------------

Administrators can update files in https://github.com/lsst-dm/panda-conf/tree/main/panda_env to
create different pilot environments. Here are the steps:

- Update https://github.com/lsst-dm/panda-conf/blob/main/panda_env/panda_env_install.sh and related
  files. This command is executed by CVMFS admins to deploy different pilot environments to CVMFS.
  During updating this file, it's good to make sure it can run successfully.

- Draft a new release in https://github.com/lsst-dm/panda-conf/releases.

- Contact CVMFS admin Fabio Hernandez to deploy the new release to CVMFS.

- The Pilot environment will be deployed to::

  /cvmfs/sw.lsst.eu/linux-x86_64/panda_env
  /cvmfs/sw.lsst.eu/almalinux-x86_64/panda_env (new)
