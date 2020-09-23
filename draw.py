import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
import imageio


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.t1 = nn.Parameter(torch.tensor(-0.7, dtype=torch.float), requires_grad=True)
        self.t2 = nn.Parameter(torch.tensor(3.4, dtype=torch.float), requires_grad=True)

    def forward(self, x):
        return torch.sin(3*self.t1)+self.t2-0.5


def f(logits, y_true):
    return logits


input_x = torch.tensor([0.5, 0.6], dtype=torch.float)
input_y = torch.tensor(0.8, dtype=torch.float)


def train():
    model = Model()
    # SGD, RMSprop, Adagrad, Adadelta, Adam, AdamW, ASGD
    optimizer = optim.Adagrad(model.parameters())
    a = []
    b = []
    a.append(model.t1.data.item())
    b.append(model.t2.data.item())
    for iter in range(100):
        optimizer.zero_grad()
        y_pred = model(input_x)
        loss = f(y_pred, input_y)
        loss.backward()
        optimizer.step()
        print('iter={}, loss={}, params=[{}, {}]'.format(iter, loss, model.t1, model.t2))
        a.append(model.t1.data.item())
        b.append(model.t2.data.item())
    return a, b


def draw(a=None, b=None):
    # x1 = input_x[0].item()
    # x2 = input_x[1].item()
    # y = input_y.item()
    # plt.ylim(0, 5)
    # plt.xlim(-1.5, 1.5)
    color_value = 1   # loss 1 -> 0, line white -> black
    for loss_value in np.arange(0, 2, 0.1):
        t1 = np.arange(-2, 2, 0.001)
        t2 = 0.5+loss_value - np.sin(3*t1)
        plt.plot(t1, t2, color=(color_value, color_value, color_value))
        # t2 = -np.sqrt((loss_value-t1*t1/0.25)*20)
        # plt.plot(t1, t2, color=(color_value, color_value, color_value))
        color_value -= 0.05

    if a is None and b is None:
        plt.show()
    else:
        iter = 0
        for aa, bb in zip(a, b):
            plt.scatter(aa, bb, c='g', linewidths=0.01)
            plt.title('Adagrad')
            plt.savefig('fig/pic-{}.jpg'.format(iter))
            iter += 1


a, b = train()
draw(a, b)
# draw()

frames = []
for image_name in ['fig/pic-'+str(iter)+'.jpg' for iter in range(100)]:
    frames.append(imageio.imread(image_name))
imageio.mimsave('Adagrad-default.gif', frames, 'GIF', duration=0.01)
