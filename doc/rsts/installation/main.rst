Install ReNomRG
===============

ReNomRG requires following python modules.

Install by pip.
~~~~~~~~~~~~~~~~

You can install ReNomRG by ``pip`` command. This is the simplest way for installation.


  .. code-block:: shell

      pip install https://grid-devs.gitlab.io/ReNomRG/bin/renom_rg-0.1b0-py3-none-any.whl


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
