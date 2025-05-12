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
schedule the job to *<site>_Rubin_8G* which has minRSS 4GB and maxRSS 8GB.

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

Another special queue ``<site>_Rubin_Multi`` is used to manage jobs which requests more than
1 core. If the number of requested cores is more than 1, panda will automatically schedule jobs
to this panda queue. The maximum memory per core is 500 GB / number of Cores.

PanDA queues
------------

There are 6 PanDA production queues and 1 test queue at every site. The table below listed the PanDA queues
and their corresponding attributes.

The ``<site>`` can be ``SLAC`` (USDF), ``CC-IN2P3`` (FrDF), ``LANCS`` (UKDF) and ``RAL`` (UKDF).

``<site>_TEST`` is a PanDA/IDDS developer queue in which there are no guarantees about stability
and uptimes and as such should not be used for regular runs

.. list-table:: PanDA Queues
   :widths: 50 25 25 25 25 25
   :header-rows: 1

   * - PanDA Queue
     - minRSS
     - maxRSS
     - Harvester mode
     - Brokerage
     - nCores
   * - <site>_Rubin_4G
     - 0GB
     - 4GB
     - pull
     - on
     - 1
   * - <site>_Rubin_8G
     - 4GB
     - 8GB
     - pull
     - on
     - 1
   * - <site>_Rubin_12G
     - 8GB
     - 12GB
     - pull
     - on
     - 1
   * - <site>_Rubin_16G
     - 12GB
     - 16GB
     - pull
     - on
     - 1
   * - <site>_Rubin_20G
     - 16GB
     - 20GB
     - pull
     - on
     - 1
   * - <site>_Rubin_24G
     - 20GB
     - 24GB
     - pull
     - on
     - 1
   * - <site>_Rubin_28G
     - 24GB
     - 28GB
     - pull
     - on
     - 1
   * - <site>_Rubin_32G
     - 28GB
     - 32GB
     - pull
     - on
     - 1
   * - <site>_Rubin_Extra_Himem
     - 32GB
     - 500GB
     - push
     - on
     - 1
   * - <site>_Rubin_merge
     - 0GB
     - 500GB
     - push
     - off
     - 1 (>=1)
   * - <site>_Rubin_Multi
     - 0GB
     - 500GB
     - push
     - off
     - >=2
   * - *<site>_Test*
     - 0GB
     - 4GB
     - pull
     - off
     - 1


Note: In the table above, maxRSS 4G means 4000 and minRSS 4G means 4001. So that the current panda queue
and the previous panda queue don't have overlaps.

For **<site>_Rubin_Merge**, the default number of cores is 1. If the user specifies more than 1 cores,
it will user the number of cores defined by users.

For **<site>_Rubin_Multi**, when users request more than 1 core for a job, PanDA will automatically schedule
jobs to this queue. Currently the *requestMemory* is memory per core. So if the nCores is big, it's good to
make sure the total memory not too big (if the total memory is more than 500G, it will not be able to schedule
the job).

For **SLAC_Rubin_Extra_Himem** and **SLAC_Rubin_merge**, the maxRSS is 500 GB based on the site settings.

For **LANCS_Rubin_Extra_Himem** and **LANCS_Rubin_merge**, the maxRSS is 192 GB based on the site settings.

For **CC-IN2P3_Rubin_Extra_Himem** and **CC-IN2P3_Rubin_merge**, the maxRSS is unknown currently.
