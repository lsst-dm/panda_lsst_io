Data Facilities
================

Currently Rubin mainly has 3 Data Facilities (DF): USDF (SLAC), FrDF (IN2P3) and UKDF (LANCS and RAL).
These 3 DFs are fully operational with storages and computing resources. Here we will only introduce
the computing resources attached in PanDA system.
In addition, a Google based Interim Data Facility (IDF) is also availale. Currently IDF doesn't run jobs.
However, users can login to IDF to submit jobs.


General
--------
In the table below, the minRSS and maxRSS means the range of required memory.
``RSS(resident set size)`` is the portion of memory occupied by a process
that is held in main memory (RAM). BPS ``requestMemory`` will be mapped to
``RSS`` requirements in PanDA.
For example, for a Rubin job with "requestMemory: 5000" (5000MB), PanDA will
schedule the job to *<site>_Rubin_medium* which has minRSS 4GB and maxRSS 8GB.

The PanDA system uses pilot to manage user jobs. A pilot is a wrapper or an agent
which manages to setup pre-environment, monitor the user jobs, upload logs to
global storages and manages other site specific settings. The PanDA system uses
Harvester to manage the pilots. It can work with ``pull`` and ``push`` mode (See *Overview*).

The concept behind the definitions of the PanDA queues at <site> is for efficient use of the
slurm cluster, to balance time efficiency for quick jobs with memory efficiency for large memory job.

There is another special queue ``<site>_Rubin_Merge``, its memory range is from 0GB to
500GB (The maximum memory one machine at SLAC can provide). Because of its special
requirements, this is the only queue that currently must be specified by name. Internally,
it is defined as "brokeroff" which means PanDA does not use the job requirements to match
to a queue. Instead this queue only accepts jobs that have requested the queue by name.

PanDA queues
------------

There are 6 PanDA production queues and 1 test queue at every site. The table below listed the PanDA queues
and their corresponding attributes.

The ``<site>`` can be ``SLAC`` (USDF), ``CC-IN2P3`` (FrDF) and ``LANCS`` (UKDF).

``<site>_TEST`` is a PanDA/IDDS developer queue in which there are no guarantees about stability
and uptimes and as such should not be used for regular runs

.. list-table:: PanDA Queues
   :widths: 50 25 25 25 25
   :header-rows: 1

   * - PanDA Queue
     - minRSS
     - maxRSS
     - Harvester mode
     - Brokerage
   * - <site>_Rubin
     - 0GB
     - 4GB
     - pull
     - on
   * - <site>_Rubin_Medium
     - 4GB
     - 8GB
     - pull
     - on
   * - <site>_Rubin_Himem
     - 8GB
     - 16GB
     - pull
     - on
   * - <site>_Rubin_Big_Himem
     - 16GB
     - 32GB
     - pull
     - on
   * - <site>_Rubin_Extra_Himem
     - 32GB
     - 500GB
     - push
     - on
   * - <site>_Rubin_merge
     - 0GB
     - 500GB
     - push
     - off
   * - *<site>_Test*
     - 0GB
     - 4GB
     - pull
     - off


For **SLAC_Rubin_Extra_Himem** and **SLAC_Rubin_merge**, the maxRSS is 500 GB based on the site settings.
For **LANCS_Rubin_Extra_Himem** and **LANCS_Rubin_merge**, the maxRSS is 192 GB based on the site settings.
For **CC-IN2P3_Rubin_Extra_Himem** and **CC-IN2P3_Rubin_merge**, the maxRSS is unknown currently.
