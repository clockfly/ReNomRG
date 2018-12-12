Introduction
============

ReNomRG is a GUI tool & Python API for building regression models of numerical data, time series data.
Only numerical data is available in current version.

1. Concept
----------

.. ユーザが自分自身で目的に沿ったAIモデルを作れるようにすること.

In recent years, with the progress of deep learning technology, the development of AI related system has made a great progress.
ReNom has already provided ReNomIMG for image recognition and ReNomTDA for data analysis as an application. And ReNomRG will be an application to create a regression model using numerical data.
This makes it possible to easily develop a demand prediction model and construct a regression model that predicts target variables by using production equipment of each company or data of ERP (mission critical business system).It will lead to efficiency improvement.
In addition, ReNomRG uses the GraphCNN technology and in many cases realizes accuracy exceeding the machine learning method.

2. What ReNomRG provides you.
-------------------------------

ReNomRG provides gui tool and python api.

GUI tool
~~~~~~~~

Using the ReNomRG GUI tool, it is possible to build a regression model that predicts future variables for several hours and days later, based on numerical data and time series data.
Users can evaluate the developed model and manage multiple models on the interface. What users have to do are prepare training data, set train configuration and push run button.

Python API
~~~~~~~~~~

ReNomRG API has a layer that performs graph-convolution and a utility that selects close variables which have similarity.
