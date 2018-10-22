import renom as rm
from renom_rg.api.regression import Regression


class GraphCNN(rm.Conv2d):

    def __init__(self, channel, feature_graph, neighbors=5):
        super(GraphCNN, self).__init__(channel=channel, filter=(1, neighbors))
        self.feature_graph = feature_graph

    def forward(self, x):
        x = x[:, :, :, 0]
        x = x[:, :, self.feature_graph]
        return super(GraphCNN, self).forward(x)


class GCNet(rm.Model):
    def __init__(self, feature_graph, fc_unit=100, neighbors=5, channels=(10, 20)):
        super(GCNet, self).__init__()
        self.gc1 = GraphCNN(channel=channels[0], neighbors=neighbors, feature_graph=feature_graph)
        self.gc2 = GraphCNN(channel=channels[1], neighbors=neighbors, feature_graph=feature_graph)
        self.fc1 = rm.Dense(fc_unit)
        self.fc2 = rm.Dense(1)
        self.dropout = rm.Dropout(dropout_ratio=0.01)

    def forward(self, x):
        h = rm.relu(self.gc1(x))
        h = self.dropout(h)
        h = rm.relu(self.gc2(h))
        h = self.dropout(h)
        h = rm.flatten(h.reshape(h.shape[0], -1, h.shape[1]))
        h = self.dropout(rm.relu(self.fc1(h)))
        h = self.fc2(h)
        return h
