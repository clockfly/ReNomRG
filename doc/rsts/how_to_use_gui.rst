How to Use ReNomRG GUI tool
===========================

Start the Application
---------------------

ReNomRG is a single page web application.
If your installation have done successfully,
you can run application in any directory with following commands.

.. code-block :: shell

    cd workspace # Workspace can be any directory.
    renom_rg # This command will starts ReNomRG GUI server.

For the command ``renom_rg``, you can give following arguments.

* --host : This specifies server address.
* --port : This specifies port number of the server.

For example, following code runs ReNomRG with port 8888.

.. code-block :: shell

    renom_rg --port 8888 # Running ReNomRG with port 8888

If the application server runs, open web browser and type the
server address to the address bar like this.

.. image:: /_static/image/server_start.png
.. image:: /_static/image/browser.png

Then the application will be appeared.

Place your dataset
------------------

When the server starts, ``datasrc``, ``storage``, ``scripts`` and ``alembic`` directories
and ``alembic.ini`` file will be created in the server running directory.

The directory structure is below.

  .. code-block :: shell

    <server_start_directory>
        └── alembic.ini        # database setting file.
        └── alembic
        |   └── versions       # database migration files.
        |   └── env.py         # database environment file.
        └── storage
        |   └── storage.db     # default database(sqlite3).
        |   └── trained_weight # weights for regression models.
        └── datasrc
        |   └── data.pickle    # pickle data for train & validation.
        |   └── prediction_set
        |       └── pred.pickle # pickle data for prediction.
        └── scripts
            └── userdefmodel.py # scripts for user defined model.(available any name.)

The data that can be read with ReNomRG beta must be named "data.pickle" and "pred.pickle".

Format of the data
~~~~~~~~~~~~~~~~~~

The format of input file is pickled pandas.DataFrame object.

Create Regression Model
-----------------------

So far, the server and dataset are prepared. Let's build a regression model.
For building a model, you have to specify ``dataset`` and ``hyper parameters``.

Create Dataset
~~~~~~~~~~~~~~

For training a machine learning model, you have to prepare training dataset and validation dataset.
Training dataset is used for training model, and validation dataset is used for evaluating a model in terms of how accurately predicted value is.
In ReNomRG, training dataset and validation dataset will be randomly sampled from the data that is in the datasrc directory.

.. image:: /_static/image/dataset.png

According to the above figure, you can create dataset from the datasrc. Once the dataset is created, its content will not be changed.
Please press new button.

.. image:: /_static/image/add.png

The following page will be appeared.

.. image:: /_static/image/setting_dataset.png

As you can see, you can specify the dataset name, ''description'', ratio of training data, feature scaling and Valiables.
After filling all forms, push the confirm button to confirm the dataset.

.. image:: /_static/image/setting_dataset_confirm.png

Then following graph will appear. You can confirm total number of data and ratio of training data contained in the dataset and the histogram of the objective variable.
For saving the dataset, push the save button.
You can confirm created datasets in the dataset page. To go to the dataset page, please follow the figure below.

.. image:: /_static/image/menu_dataset.png

.. image:: /_static/image/dataset_page.png

When you click on each dataset row, you can confirm the number of data contained in them, the number of teacher data of each variable, the histogram of the objective variable.


Hyper parameter setting
~~~~~~~~~~~~~~~~~~~~~~~

All the materials have been completed so far. Let's create a model and train it.
To create a model, press the + New button.
The model setting hyper parameter appears as shown in the figure below.

.. image:: /_static/image/setting_params.png


As you can see in figure above, you can specify the following parameters:

Dataset Name: Dataset for training.

Architecture:
Regression algorithm.
C-GCNN selects variables for convolution based on correlation coefficient between variables.
Kernel-GCNN selects variables for convolution based on similarities between variables obtained from Gaussian kernel.
DBSCAN-GCNN selects variables for convolution based on the Euclidean distance between variables.
Random Forest is an ensemble learning (machine learning algorithm) using multiple models (decision trees).
XGBoost is an ensemble learning (machine learning algorithm) that combines Gradient Boosting and Random Forests.

Training loop setting:
Batch size and number of training.
Batch Size,
Total Epoch.

Graph Comvolution Params:
Number of neighbors is parameters of Graph Convolution.
The number of neighbors used when data are expanded as if they were images.

Random Forest (XGBoost) Params:
Number of trees is number of decision trees.
Maximum Depth is depth of decision tree.

Training Model
~~~~~~~~~~~~~~

When the hyper parameter setting is completed, press the [Run] button to start the training.
When training begins, the model is displayed in the model list and a progress bar appears.

.. image:: /_static/image/progress.png

Uninstall ReNomRG
-----------------

ReNomRG can be uninstalled with the following pip command.

.. code-block :: shell

    pip uninstall renom_rg
