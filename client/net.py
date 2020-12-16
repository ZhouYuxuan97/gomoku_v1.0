import numpy as np
import pickle as pk
import torch as tr
import torch.nn as nn
import torch.optim as optim
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh


class LeNet(nn.Module):
    def __init__(self, board_size=10):
        super(LeNet, self).__init__()
        self.conv = nn.Sequential(  # e.g. input_size=(2*10*10)
            nn.Conv2d(2, 6, 3, 1, 1),  # padding=1 to keep output_size=input_size
            nn.Sigmoid(),  # input_size=(6*10*10)
            nn.MaxPool2d(kernel_size=2, stride=2),  # output_size=(6*5*5)
        )
        self.fc1 = nn.Sequential(
            nn.Linear(int(6 * board_size ** 2 / 4), 120),
            nn.Sigmoid()
        )
        self.fc2 = nn.Sequential(
            nn.Linear(120, 84),
            nn.Sigmoid()
        )
        self.fc3 = nn.Linear(84, 1)

    def forward(self, x):
        x = self.conv(x)
        # flat
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x


def calculate_loss(net, x, y_targ):
    return net(x), tr.sum((net(x) - y_targ) ** 2)


def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return y, e


net = LeNet()
optimizer = optim.Adam(net.parameters())

if __name__ == "__main__":
    # set board size below
    board_size = 10
    epoch_num = 800
    print(tr.cuda.is_available())
    with open("data%d.pkl" % board_size, "rb") as f:
        (x, y_targ) = pk.load(f)

    shuffle = np.random.permutation(range(len(x)))  # shuffle 0-[len(x)-1]
    split = int(0.8 * len(x))
    train, test = shuffle[:split], shuffle[split:]
    x_train = x[train]
    y_train = y_targ[train]
    x_test = x[test]
    y_test = y_targ[test]
    print(x_train.shape, x_test.shape)
    print(y_train.shape, y_test.shape)

    train_loss, test_loss = [], []
    for epoch in range(epoch_num):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 50 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle) - split))
        test_loss.append(e_test.item() / split)

    tr.save(net.state_dict(), "../model%d.pth" % board_size)

    import matplotlib.pyplot as pt

    pt.plot(train_loss, 'b-')
    pt.plot(test_loss, 'r-')
    pt.legend(["Train", "Test"])
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    pt.show()

    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(), 'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(), 'ro')
    pt.legend(["Train", "Test"])
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    pt.show()
