How to Use ReNomRG GUI tool
===========================

Start the Application
---------------------

ReNomRG is a single page web application.
You can run application in ReNomRG directory with ReNomRG beta version.

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

.. image:: /_static/image/server_start.png
.. image:: /_static/image/browser.png

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
~~~~~~~~~~~~~~~~~~

In the ReNomRG beta version, you can enter a file that pickled pandas.DataFrame into the application.


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

.. image:: /_static/image/dataset.png

The following page will be appeared.

.. image:: /_static/image/setting_dataset.png

As you can see, you can specify the dataset name, ''description'' and ratio of training data.
After filling all forms, push the confirm button to confirm the dataset.

.. image:: /_static/image/setting_dataset_confirm.png

Then following graph will appear. You can confirm total number of data and ratio of training data contained in the dataset and the histogram of the objective variable.
For saving the dataset, push the save button.
You can confirm created datasets in the dataset page. To go to the dataset page, please follow the figure below.

.. image:: /_static/image/menu_dataset.png

.. image:: /_static/image/dataset_page.png

You can see that the dataset page above shows that three datasets have already been created. When you click on each data set name, you can confirm the number of data contained in them, the number of teacher data of each variable, the histogram of the objective variable.


Hyper parameter setting
~~~~~~~~~~~~~~~~~~~~~~~

All the materials have been completed so far. Let's create a model and train it.
To create a model, press the + New button.
The model setting hyper parameter appears as shown in the figure below.

.. image:: /_static/image/setting_params.png


As you can see in figure above, you can specify the following parameters:
Dataset Name: Dataset for training.

CNN architecture: Regression algorithm.
C-GCNN selects variables for convolution based on correlation coefficient between variables.
Kernel-GCNN selects variables for convolution based on similarities between variables obtained from Gaussian kernel.
DBSCAN-GCNN selects variables for convolution based on the Euclidean distance between variables.

Training loop setting: Number of training and batch size.
Batch Size
Total Epoch

Graph Comvolution Params
Number of neighbors is parameters of Graph Convolution. The number of neighbors used when data are expanded as if they were images.

Training Model
~~~~~~~~~~~~~~

When the hyper parameter setting is completed, press the [Run] button to start the training.
When training begins, the model is displayed in the model list and a progress bar appears.

.. image:: /_static/image/progress.png

Uninstall ReNomRG
-----------------

.. code-block :: shell

    pip uninstall renom_rg

ReNomRG can be uninstalled with the following pip command.
