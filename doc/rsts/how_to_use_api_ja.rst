ReNomIMG APIの使い方
==================

グラフコンボリューション
--------------------

グラフコンボリューションは、非画像データにCNNを適応する手法です。
非画像データにCNNを適応するために、入力データを画像データに変換する必要があります。
この過程では様々な指標を選ぶことができます。

データの変換
----------

例えば、変数同士の相関を用いることができます。
はじめに、相関行列を計算します。

それから、相関が高いk個の変数の順番を取得したインデックス行列を作成します。
そして、k個の変数を一つの変数として畳み込みを行います。kはパイパーパラメータになります。

ソースコード
----------

ReNomRGはGraphCNNレイヤーと、インデックス行列を取得するためのユーティリティを提供しています。

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split

    import renom as rm
    from renom.optimizer import Adam
    from renom_rg.api.regression.gcnn import GraphCNN
    from renom_rg.api.utility.feature_graph import get_corr_graph

    # load example data
    boston = load_boston()
    X = boston.data
    y = boston.target

    # split train & prediction
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # setting hyper parameters
    epoch = 100
    batch_size = 16
    num_neighbors = 5
    channel = 10

    # get top k index of sorted correlation.
    index_matrix = get_corr_graph(X_train, num_neighbors)

    model = rm.Sequential([
        GraphCNN(feature_graph=index_matrix, channel=channel, neighbors=num_neighbors),
        rm.Relu(),
        rm.Flatten(),
        rm.Dense(1)
    ])

    optimizer = Adam()

    # training loop
    train_loss_list = []
    valid_loss_list = []

    for e in range(epoch):
        N = X_train.shape[0]
        perm = np.random.permutation(N)
        loss = 0
        total_batch = N // batch_size

        for j in range(total_batch):
            index = perm[j * batch_size: (j + 1) * batch_size]
            train_batch_x = X_train[index].reshape(-1, 1, X_train.shape[1], 1)
            train_batch_y = y_train[index]

            # Loss function
            model.set_models(inference=False)
            with model.train():
                batch_loss = rm.mse(model(train_batch_x), train_batch_y.reshape(-1, 1))

            # Back propagation
            grad = batch_loss.grad()

            # Update
            grad.update(optimizer)
            loss += batch_loss.as_ndarray()

        train_loss = loss / (N // batch_size)
        train_loss_list.append(train_loss)

        # validation
        model.set_models(inference=True)
        N = X_test.shape[0]

        valid_predicted = model(X_test.reshape(-1, 1, X_test.shape[1], 1))
        valid_loss = float(rm.mse(valid_predicted, y_test.reshape(-1, 1)))
        valid_loss_list.append(valid_loss)

        print("epoch: {}, valid_loss: {}".format(e, valid_loss))

    plt.figure(figsize=(10, 4))
    plt.plot(train_loss_list, label='loss')
    plt.plot(valid_loss_list, label='test_loss', alpha=0.6)
    plt.title('Learning curve')
    plt.xlabel("Epoch")
    plt.ylabel("MSE")
    plt.legend()
    plt.grid()
    plt.show()


.. image:: /_static/image/learning_curve.png

グラフコンボリューションは、非画像データにCNNを適応する手法です。
ReNomRGはGraphCNNレイヤーと、インデックス行列を取得するためのユーティリティを提供しています。
