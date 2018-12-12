import renom as rm
from renom_rg.api.regression import Regression


class GraphCNN(rm.Conv2d):
    """ Graph Comvolution Layer.

    Args:
        channel: The dimensionality of the output.
        feature_graph: Array of indexes for comvolution.
        neighbors: Filter size of the convolution kernel.

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
        x = x[:, :, :, 0]
        x = x[:, :, self.feature_graph]
        return super(GraphCNN, self).forward(x)


class GCNet(rm.Model):
    """ Graph Comvolution Network.

    Args:
        feature_graph: Array of indexes for comvolution.
        num_target: Number of target data.
        fc_unit: Unit size of dense layers.
        neighbors: Filter size of convolution layers.
        channels: Channel size of convolution layers.

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
