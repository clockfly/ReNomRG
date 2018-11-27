# ReNomRG v0.0

ReNom RG is model developing tool for numerical regression.

### ReNomRG
http://renom.jp/index.html

## Recommended Environment
- OS: Ubuntu 16.04
- Browser: Google Chrome(version 63.0.3239.132)
- Python: >=3.5

## Install
ReNomIMG requires ReNom.

If you haven't install ReNom, you must install ReNom from www.renom.jp.

## Install from source
For installing ReNomRG, download the repository from following url.

`git clone https://github.com/ReNom-dev-team/ReNomRG.git`

And move into ReNomRG directory.
`cd ReNomRG`

Then install all required packages.

`pip install -r requirements.txt`

And install renom module using following command.

`pip install -e .`

## How to start

1.Type following command in ReNomRG directory.

`python -m renom_rg`

## How to use

#### Where to put your data
Please put pickle data to datasrc directory. The folder structure is below.

To create datasrc directory, please start ReNomRG server according to 'How to start'.

The datasrc directory is automatically created when you start up server.

```
ReNomIMG
    └── storage
    |   └── storage.db // Database(sqlite3).
    └── datasrc
        ├── data.pickle // pickle data for train & validation.
        └── prediction_set
            └── pred.pickle // pickle data for prediction.
```

The data that can be read with ReNomRG v0.0 must be named "data.pickle" and "pred.pickle".

## Format of input data.

The format of input file is pickled pandas.DataFrame object.

## License

“ReNomRG” is provided by GRID inc., as subscribed software.  By downloading ReNomRG, you are agreeing to be bound by our ReNom Subscription agreement between you and GRID inc.
To use ReNomRG for commercial purposes, you must first obtain a paid license. Please contact us or one of our resellers.  If you are an individual wishing to use ReNomRG for academic, educational and/or product evaluation purposes, you may use ReNomRG royalty-free.
The ReNom Subscription agreements are subject to change without notice. You agree to be bound by any such revisions. You are responsible for visiting www.renom.jp to determine the latest terms to which you are bound.
