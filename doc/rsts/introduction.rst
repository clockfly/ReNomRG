Introduction
============

ReNomRG is a GUI tool & Python API for building regression models of numerical data, time series data.
Only numerical data is available in current version.

1. Concept
----------

.. ユーザが自分自身で目的に沿ったAIモデルを作れるようにすること.

The concept of ReNomRG is to allow users to create AI models according to users’ purpose.

We have achieved a steady progress in areas such as automatic driving and image analysis technology, voice application, due to the development of deep learning technology in recent years.
But in the area of B2B, data acquired from companies and production equipments are diverse and there are still many problems for learning models from certain dataset.

For example, tasks before learning include collecting training dataset of time series data and numerical data such as log data that can be acquired from plant industrial robots, programming models and other tasks such as training, evaluating the model, and so on. Hyper parameter tuning is also requires, thus many trial and error are required.

ReNomRG allows users to easily build the prediction model of target variables and prediction model for predicting state after several hours and days by using GraphCNN technology which can handle numerical data and time series data like image data.

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
