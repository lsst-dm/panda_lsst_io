##############################################
PanDA documentation repository (panda.lsst.io)
##############################################

This is the Sphinx documentation repository for `panda.lsst.io <https://panda.lsst.io>`_, the user guide for PanDA.

Contribution primer
===================

Clone the source::

    git clone https://github.com/lsst-dm/panda_lsst_io
    cd panda_lsst_io

Install `tox <https://tox.wiki/en/latest/>`__ and `pre-commit <https://pre-commit.com/>`_, which are used for running the Sphinx build and linting files, respectively::

    make init

The documentation source files are located in the ``src/`` directory.
You can run a Sphinx build through tox::

    tox -e sphinx

The built HTML site is located at ``_build/html``.

If you ever need to fully delete the Sphinx build and the tox-based virtual environments, you can run::

    make clean

You can validate that links work::

    tox -e linkcheck

Pre-commit lints files before every commit, but you can also run pre-commit on-demand::

    tox -e precommit

Viewing drafts
==============

Through GitHub Actions, this repository publishes to https://panda.lsst.io whenever the ``main`` branch is updated.
Builds of development branches are also published to the web at https://panda.lsst.io/v.

Refreshing the Python dependencies
==================================

For repeatability, this project uses Python dependencies defined in ``requirements.txt``, which are installed in virtual environments managed by tox.

If you need to update these dependencies (e.g., to get a new version of Sphinx), run::

    make update

To add a new dependency, or to change version constraints, edit ``requirements.in`` (not ``.txt``) and then run ``make update`` to create a new ``requirements.txt`` file with compiled dependencies.
