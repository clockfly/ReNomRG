Install ReNomRG
===============

Recommended Environment.
~~~~~~~~~~~~~~~~~~~~~~~~

- OS: Ubuntu 16.04
- Browser: Google Chrome(version 63.0.3239.132)
- Python: >=3.5

Requirements Packages.
~~~~~~~~~~~~~~~~~~~~~~

ReNomRG requires following python modules.

- alembic==1.0.5
- bottle==0.12.16
- SQLAlchemy==1.2.15

And ReNomRG requires ReNom.

If you haven't install ReNom, please install ReNom from  https://github.com/ReNom-dev-team/ReNom.git.

Please refer to the ReNom installation below.
https://www.renom.jp/packages/renomdl/rsts/installation/installation.html

Install by pip.
~~~~~~~~~~~~~~~

You can install ReNomRG by ``pip`` command. This is the simplest way for installation.

The Wheel package is provided at:

  .. code-block:: shell

    https://grid-devs.gitlab.io/ReNomRG/bin/renom_rg-VERSION-py3-none-any.whl

Install 0.1.0b0(beta version) is follow.

  .. code-block:: shell

      pip install https://grid-devs.gitlab.io/ReNomRG/bin/renom_rg-0.1.0b0-py3-none-any.whl


  .. note::

      This is ``linux OS`` only. If your OS is windows or MAC, please install ReNomRG
      from binary code.


Install from source.
~~~~~~~~~~~~~~~~~~~~

    If you install ReNomRG from source, Node.js is required.

    .. code-block:: shell

        git clone https://github.com/ReNom-dev-team/ReNomRG.git
        cd ReNomRG/
        pip install -r requirements.txt
        python setup.py build
        pip install -e .

    .. note ::

        This requires ``node.js``.
