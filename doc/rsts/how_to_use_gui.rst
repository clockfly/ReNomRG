How to Use ReNomRG GUI tool
===========================

Start the Application
---------------------

ReNomRG is a single page web application.
If your installation have done successfully,
you can run application in any directory with following commands.

.. code-block :: shell

    cd ReNomRG
    python -m renom_rg # This command will starts ReNomRG GUI server.

For the command ``renom_rg``, you can give following arguments.

* --host : This specifies server address.
* --port : This specifies port number of the server.

For example, following code runs ReNomRG with port 8888.

.. code-block :: shell

    python -m renom_rg --port 8888 # Running ReNomRG with port 8888

If the application server runs, open web browser and type the
server address to the address bar like this.

.. サーバ起動の画像

Then the application will be appeared.


Place your dataset
------------------

When the server starts, ``datasrc`` directory and ``storage`` directory
will be created in the server running directory.

The ``datasrc`` directory has following folder structure.

.. code-block :: shell

    datasrc/
      ├── data.pickle # pickled pandas.DataFrame for train & validation.
      └── prediction_set
            └── pred.pickle # pickled pandas.DataFrame for prediction.


The data that can be read with ReNomRG v0.0 must be named "data.pickle" and "pred.pickle".


Format of the data
~~~~~~~~~~~~~~~~~~~

The format of input file is pickled pandas.DataFrame object.


Create Regression Model
-----------------------

So far, the server and dataset are prepared. Let's build a regression model.
For building a model, you have to specify ``dataset`` and ``hyper parameters``.

Create Dataset
~~~~~~~~~~~~~~


Hyper parameter setting
~~~~~~~~~~~~~~~~~~~~~~~


Training Model
~~~~~~~~~~~~~~


Uninstall ReNomRG
-----------------
