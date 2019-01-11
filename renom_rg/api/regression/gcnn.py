import renom as rm
from renom_rg.api.regression import Regression


class GraphCNN(rm.Conv2d):
    """ Graph Comvolution Layer.

    Args:
        channel (int): The dimensionality of the output.
        feature_graph (array): Array of indexes for comvolution.
        neighbors (int): Filter size of the convolution kernel.

    Example:
        >>> import renom as rm
        >>> import numpy as np
        >>> from renom_rg.api.regression.gcnn import GraphCNN
        >>> n, c, variables, neighbors = (2, 10, 20, 5)
        >>> x = rm.Variable(np.random.rand(n, c, variables, neighbors))
        >>> feature_graph = np.random.rand(0, variables-1, (variables, neighbors))
        >>> model = GraphCNN(15, feature_graph)
        >>> t = model(x)
        >>> t.shape
        (2, 15, 20, 1)
    """

    def __init__(self, channel, feature_graph, neighbors=5):
        super(GraphCNN, self).__init__(channel=channel, filter=(1, neighbors))
        self.feature_graph = feature_graph

    def forward(self, x):
        """Performs forward propagation.
        This function can be called using ``__call__`` method.
        See following example of method usage.

        Args:
            x (ndarray): Input data as ndarray.

        Returns:
            (Node): predicted values for input ndarray.

        Example:
            >>> import renom as rm
            >>> import numpy as np
            >>> from renom_rg.api.regression.gcnn import GraphCNN
            >>> n, c, variables, neighbors = (2, 10, 20, 5)
            >>> x = rm.Variable(np.random.rand(n, c, variables, neighbors))
            >>> feature_graph = np.random.rand(0, variables-1, (variables, neighbors))
            >>> model = GraphCNN(15, feature_graph)
            >>> t = model.forward(x)
            >>> t.shape
            (2, 15, 20, 1)
        """
        x = x[:, :, self.feature_graph, 0]
        return super(GraphCNN, self).forward(x)


class GCNet(rm.Model):
    """ Graph Comvolution Network.
        This network has 3 GraphCNN layer and 2 FC layer and 1 output layer.

    Args:
        feature_graph (array): Array of indexes for comvolution.
        num_target (int): Number of unit size of output layer.
        fc_unit (tuple): Tuple of unit size of dense layers.
        neighbors (int): Filter size of convolution layers.
        channels (tuple): Tuple of channel size of convolution layers.

    Example:
        >>> import renom as rm
        >>> import numpy as np
        >>> from renom_rg.api.regression.gcnn import GCNet
        >>> n, c, variables, neighbors = (2, 10, 20, 5)
        >>> x = rm.Variable(np.random.rand(n, c, variables, neighbors))
        >>> feature_graph = np.random.rand(0, variables-1, (variables, neighbors))
        >>> model = GCNet(feature_graph)
        >>> t = model(x)
        >>> t.shape
        (2, 1)
    """

    def __init__(self, feature_graph, num_target=1, fc_unit=(100, 50), neighbors=5, channels=(10, 20, 20)):
        super(GCNet, self).__init__()
        self.gc1 = GraphCNN(channel=channels[0], neighbors=neighbors, feature_graph=feature_graph)
        self.gc2 = GraphCNN(channel=channels[1], neighbors=neighbors, feature_graph=feature_graph)
        self.gc3 = GraphCNN(channel=channels[2], neighbors=neighbors, feature_graph=feature_graph)
        self.fc1 = rm.Dense(fc_unit[0])
        self.fc2 = rm.Dense(fc_unit[1])
        self.fc3 = rm.Dense(num_target)
        self.dropout = rm.Dropout(dropout_ratio=0.01)

    def forward(self, x):
        """Performs forward propagation.
        This function can be called using ``__call__`` method.
        See following example of method usage.

        Args:
            x (ndarray): Input data as ndarray.

        Returns:
            (Node): predicted values for input ndarray.

        Example:
            >>> import renom as rm
            >>> import numpy as np
            >>> from renom_rg.api.regression.gcnn import GCNet
            >>> n, c, variables, neighbors = (2, 10, 20, 5)
            >>> x = rm.Variable(np.random.rand(n, c, variables, neighbors))
            >>> feature_graph = np.random.rand(0, variables-1, (variables, neighbors))
            >>> model = GCNet(feature_graph)
            >>> t = model.forward(x)
            >>> t.shape
            (2, 1)

        """
        h = rm.relu(self.gc1(x))
        h = self.dropout(h)
        h = rm.relu(self.gc2(h))
        h = self.dropout(h)
        h = rm.relu(self.gc3(h))
        h = self.dropout(h)
        h = rm.flatten(h.reshape(h.shape[0], -1, h.shape[1]))
        h = self.dropout(rm.relu(self.fc1(h)))
        h = self.dropout(rm.relu(self.fc2(h)))
        h = self.fc3(h)
        return h

    def predict(self, x):
        """Perform prediction.
        Execute forward function in inference mode.

        Args:
            x (ndarray): Input data as ndarray.

        Returns:
            (Node): predicted values for input ndarray.

        Example:
            >>> import renom as rm
            >>> import numpy as np
            >>> from renom_rg.api.regression.gcnn import GCNet
            >>> n, c, variables, neighbors = (2, 10, 20, 5)
            >>> x = rm.Variable(np.random.rand(n, c, variables, neighbors))
            >>> feature_graph = np.random.rand(0, variables-1, (variables, neighbors))
            >>> model = GCNet(feature_graph)
            >>> t = model.predict(x)
            >>> t.shape
            (2, 1)
        """
        self.set_models(inference=True)
        return self.forward(x.reshape(-1, 1, x.shape[1], 1))
