import torch
from torch import nn
import numpy as np
from stats import stats
from utils import add_op
from data_loader import data_load
from label_loader import label_load

class Stock_LSTM(nn.Module):
    def __init__(self):
        super(Stock_LSTM, self).__init__()

        self.rnn = nn.LSTM(     # LSTM
            input_size=6,       # 每一天的输入
            hidden_size=16,     # rnn hidden unit
            num_layers=2,       # 有几层 RNN layers
            batch_first=True,   # input & output 会是以 batch size 为第一维度的特征集 e.g. (batch, time_step, input_size)
        )

        self.out = nn.Linear(16, 1)    # 输出层

    def forward(self, x):
        # x shape (batch, time_step, input_size)
        # r_out shape (batch, time_step, output_size)
        # h_n shape (n_layers=1, batch, hidden_size)   LSTM 有两个 hidden states, h_n 是输出, h_c 是记忆
        # h_c shape (n_layers=1, batch, hidden_size)
        r_out, (h_n, h_c) = self.rnn(x, None)   # None 表示 hidden state 会用全0的 state
        out = self.out(r_out)
        return out

snn = Stock_LSTM()
print(snn)

labels = stats("./data", stat_op = add_op, data_fn=label_load, id="0600010", year=None)
data = stats("./data", stat_op = add_op, data_fn=data_load, id="0600010", year=None)

# 训练数据集
train_label = torch.tensor([labels])[:,1:-1000,:]
train_x = torch.tensor([data], requires_grad=True)[:,:-1001,:]

# 测试数据集
test_label = torch.tensor([labels])[:,-1000:,:]
test_x = torch.tensor([data], requires_grad=True)[:,-1001:-1,:]

print("train label size: " + str(train_label.size()))
print("train data size : " + str(train_x.size()))

print("test label size : " + str(test_label.size()))
print("test data size  : " + str(test_x.size()))


EPOCH = 1000
optimizer = torch.optim.Adam(snn.parameters(), lr=0.01)   # optimize all parameters
loss_func = nn.MSELoss()

# training and testing
for epoch in range(EPOCH):
    
    output = snn(train_x)               # output
    loss = loss_func(output, train_label)   # cross entropy loss
    optimizer.zero_grad()           # clear gradients for this training step
    loss.backward()                 # backpropagation, compute gradients
    optimizer.step()                # apply gradients

    test_output = snn(test_x)                   # (samples, time_step, input_size)
    error = loss_func(test_output, test_label)
    print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test error: %.2f' % error)

torch.save(snn, "./net/NN001")
print('Model Saved')