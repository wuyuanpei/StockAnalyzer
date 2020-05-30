import torch
from torch import nn
import numpy as np
from stats import stats
from utils import add_op
from data_loader import data_load
from Anim import DynamicUpdate
from view import draw_results

# 预测股票趋势的RNN模型,模型的架构为LSTM加上FC
class Stock_LSTM(nn.Module):

    # 构造RNN模型
    # input_size:   每一天的输入向量的大小, 默认为6: start, end, highest, lowest, hand, rate
    # hidden_size:  LSTM 隐藏向量层大小
    # num_layers:   LSTM 层数
    def __init__(self, input_size=6, hidden_size=32, num_layers=1):
        super(Stock_LSTM, self).__init__()

        self.rnn = nn.LSTM(     # LSTM
            input_size=input_size,       # 每一天的输入
            hidden_size=hidden_size,      # rnn hidden unit
            num_layers=num_layers,       # 有几层 RNN layers
            batch_first=True,   # input & output 会是以 batch size 为第一维度的特征集 e.g. (batch, time_step, input_size)
        )

        self.out = nn.Linear(hidden_size, 1)    # 输出层

    def forward(self, x):
        # x shape (batch, time_step, input_size)
        # r_out shape (batch, time_step, output_size即1)
        # h_n shape (n_layers=1, batch, hidden_size)   LSTM 有两个 hidden states, h_n 是输出, h_c 是记忆
        # h_c shape (n_layers=1, batch, hidden_size)

        r_out, (h_n, h_c) = self.rnn(x, None)   # None 表示 hidden state 会用全0的 state

        r_out = self.out(r_out)
        
        return r_out

# 训练该LSTM模型
# 训练样本为某一只股票从1991到2019的数据
# snn:      训练模型, Stock_LSTM的对象
# id:       股票的id
# epoch:    训练epoch
# lr:       Adam算法learning rate
# save_path:储存目录与文件名
# real_draw:是否实时绘制Train和Test Loss
def train(snn, id, epoch = 250, lr = 0.05, save_path = "./net/NN", real_draw = True):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    snn.to(device)

    items = []

    for i in range(1991,2020):
        item = stats("./data", stat_op = add_op, data_fn=data_load, id=id, year=str(i))
        if item is None:
            print("year "+str(i)+" is not found!")
        else:
            items += item

    optimizer = torch.optim.Adam(snn.parameters(), lr=lr)   # optimize all parameters
    loss_func = nn.MSELoss()

    d1 = DynamicUpdate(epoch, 12, "training loss")
    d2 = DynamicUpdate(epoch, 12, "testing loss")
    d1.on_launch()
    d2.on_launch()
    # training and testing
    for epoch in range(epoch):

        average_loss = 0

        for data in items:
        
            labels = torch.FloatTensor([data[1:,5:]]).to(device) # Label

            # Normalize data
            data = (data - np.mean(data, axis=0, keepdims=True))/np.std(data, axis=0, keepdims=True)
        
            inputs = torch.FloatTensor([data[:-1,:]]).to(device)
        
            outputs = snn(inputs)               # output

            loss = loss_func(outputs, labels)   # MSE loss

            optimizer.zero_grad()           # clear gradients for this training step
            loss.backward()                 # backpropagation, compute gradients
            optimizer.step()                # apply gradients

            average_loss += loss.item()

        train_loss = average_loss/len(items)
        print('Epoch: ', epoch, '| train loss: %.4f' %train_loss)
        d1.draw(train_loss)
        d2.draw(validate(snn, id))


    torch.save(snn, save_path)
    print('Model Saved at '+save_path)
    validate(snn, id, draw=True)

# 测试该LSTM模型, 打印测试MSELoss
# 测试使用2020的数据
# snn:      模型, Stock_LSTM的对象
# id:       股票的id
# draw:     是否画出k线图和预测结果比对
# return:   测试MSELoss
def validate(snn, id, draw=False):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data = stats("./data", stat_op = add_op, data_fn=data_load, id=id, year="2020", v=False)[0]
    labels = torch.FloatTensor([data[1:,5:]]).to(device) # Label
    data = (data - np.mean(data, axis=0, keepdims=True))/np.std(data, axis=0, keepdims=True)
    inputs = torch.FloatTensor([data[:-1,:]]).to(device)

    outputs = snn(inputs)

    loss = nn.MSELoss()(outputs, labels)

    predictions = outputs.squeeze().tolist()
    predictions.insert(0, 0)

    print("Test Loss:"+str(loss.item()))

    if draw:
        draw_results(id, "2020", prediction=predictions)

    return loss.item()

if __name__ == "__main__":
    snn = Stock_LSTM(input_size=6, hidden_size=32, num_layers=1)
    train(snn, id="0600000", epoch = 250, lr = 0.01, save_path = "./net/NN")