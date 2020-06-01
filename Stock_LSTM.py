import torch
from torch import nn
import torch.nn.functional as F
import numpy as np
import random
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
    # hidden_linear:FC层隐藏向量大小
    def __init__(self, input_size=6, hidden_size=32, num_layers=1, hidden_linear=16):
        super(Stock_LSTM, self).__init__()

        self.rnn = nn.LSTM(     # LSTM
            input_size=input_size,       # 每一天的输入
            hidden_size=hidden_size,      # rnn hidden unit
            num_layers=num_layers,       # 有几层 RNN layers
            batch_first=True,   # input & output 会是以 batch size 为第一维度的特征集 e.g. (batch, time_step, input_size)
        )

        self.fc1 = nn.Linear(hidden_size, hidden_linear) # FC层
        self.fc2 = nn.Linear(hidden_linear, 1) # 输出层

    def forward(self, x):
        # x shape (batch, time_step, input_size)
        # r_out shape (batch, time_step, output_size即1)
        # h_n shape (n_layers=1, batch, hidden_size)   LSTM 有两个 hidden states, h_n 是输出, h_c 是记忆
        # h_c shape (n_layers=1, batch, hidden_size)

        r_out, (h_n, h_c) = self.rnn(x, None)   # None 表示 hidden state 会用全0的 state
        
        r_out = self.fc1(r_out)
        r_out = torch.tanh(r_out)
        r_out = self.fc2(r_out)
        return r_out

# 训练该LSTM模型
# 训练样本为某一只股票从1991到2019的数据
# snn:          训练模型, Stock_LSTM的对象
# train_data:   训练数据, 字典: "id":(starty, endy)
#               id:(str)       股票的id
#               starty:(int)   训练数据的开始年份, 包含, 建议从第一个有完整数据的年份开始
#               endy:(int)     训练数据的结束年份, 不包含, 默认2020, 即训练到2019年为止
# test_data:    测试数据, 字典: "id":(starty, endy); 如果是None, 则从train_data中随机抽取1/5作为测试数据
# epoch:    训练epoch
# lr:       Adam算法learning rate
# save_path:储存目录与文件名
# real_draw:是否实时绘制Train和Test Loss
def train(snn, train_data, test_data=None, epoch = 250, lr = 0.05, save_path = "./net/NN", real_draw = True):

    print("LOADING TESTING DATA...")
    # 随机抽取一些作为测试数据
    if test_data is None:
        test_data = {}
        k_list = random.sample(train_data.keys(), len(train_data)//5)
        print(str(k_list) + " is used as testing set")
        for k in k_list:
            v = train_data.pop(k)
            test_data[k] = v

    # 找到数据数组
    test_data_items = []
    for tid, (tstarty, tendy) in test_data.items():
        for i in range(tstarty,tendy):
            test_data_item = stats("./data", stat_op = add_op, data_fn=data_load, id=tid, year=str(i), v=False)
            if test_data_item is None:
                pass
                #print("year "+str(i)+" is not found!")
            else:
                test_data_items += test_data_item

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    snn.to(device)


    print("LOADING TRAINING DATA...")
    items = []

    for id, (starty, endy) in train_data.items():
        for i in range(starty,endy):
            item = stats("./data", stat_op = add_op, data_fn=data_load, id=id, year=str(i), v=False)
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

    print("Training Start")
    # training and testing
    for epoch in range(epoch):

        average_loss = 0
        random.shuffle(items) # shuffle the data every epoch

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

        average_loss = average_loss / len(items)
        print('Epoch: ', epoch, '| train loss: %.4f' %average_loss)
        d1.draw(average_loss)
        d2.draw(validate(snn, test_data_items))


    torch.save(snn, save_path)
    print('Model Saved at '+save_path)

    validate(snn, test_data_items)

# 测试该LSTM模型, 打印测试MSELoss
# snn:      模型, Stock_LSTM的对象
# test_data_items: 测试数据数组
# return:   测试MSELoss
def validate(snn, test_data_items):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    average_loss = 0
    for data in test_data_items:
        
        labels = torch.FloatTensor([data[1:,5:]]).to(device) # Label

        data = (data - np.mean(data, axis=0, keepdims=True))/np.std(data, axis=0, keepdims=True)
        inputs = torch.FloatTensor([data[:-1,:]]).to(device)

        outputs = snn(inputs)

        average_loss += nn.MSELoss()(outputs, labels)

        # if draw and len(test_data) == 1 and starty == endy-1:
        #     predictions = outputs.squeeze().tolist()
        #     predictions.insert(0, 0)
        #     draw_results(id, str(starty), prediction=predictions)

    average_loss /= len(test_data_items)
    print("Test Loss:"+str(average_loss.item()))

    return average_loss.item()



# 取样测试该LSTM模型, 打印测试MSELoss并绘图
# snn:      模型, Stock_LSTM的对象
# id:       股票的id
# year:     股票的年份
# return:   测试MSELoss
def sample(snn, id, year):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data = stats("./data", stat_op = add_op, data_fn=data_load, id=id, year=str(year), v=False)[0]
    labels = torch.FloatTensor([data[1:,5:]]).to(device) # Label
    data = (data - np.mean(data, axis=0, keepdims=True))/np.std(data, axis=0, keepdims=True)
    inputs = torch.FloatTensor([data[:-1,:]]).to(device)

    outputs = snn(inputs)

    loss = nn.MSELoss()(outputs, labels)

    predictions = outputs.squeeze().tolist()
    predictions.insert(0, 0)

    print("Sample Test Loss:"+str(loss.item()))

    draw_results(id, str(year), prediction=predictions)

    return loss.item()


TRAINING_DATA = {
    "0600000":(2000,2019),
    "0600004":(2004,2019),
    "0600005":(2000,2017),
    "0600006":(2000,2019),
    "0600007":(2000,2019),
    "0600008":(2001,2019),
    "0600009":(1998,2019),
    "0600010":(2002,2019),
    "0600011":(2002,2019),
    "0600012":(2003,2019),
    "0600015":(2004,2019),
}

TESTING_DATA = {
    "0600000":(2019,2020),
    "0600004":(2019,2020),
    "0600005":(2017,2018),
    "0600006":(2019,2020),
    "0600007":(2019,2020),
    "0600008":(2019,2020),
    "0600009":(2019,2020),
    "0600010":(2019,2020),
    "0600011":(2019,2020),
    "0600012":(2019,2020),
    "0600015":(2019,2020),
}

ALL_DATA = {
    "0600000":(2000,2020),
    "0600004":(2004,2020),
    "0600005":(2000,2018),
    "0600006":(2000,2020),
    "0600007":(2000,2020),
    "0600008":(2001,2020),
    "0600009":(1998,2020),
    "0600010":(2002,2020),
    "0600011":(2002,2020),
    "0600012":(2003,2020),
    "0600015":(2004,2020),
    "0600016":(2001,2020),
    "0600017":(2007,2020),
    "0600018":(2001,2020),
    "0600019":(2001,2020),
    "0600020":(2004,2020),
    "0600021":(2004,2020),
    "0600022":(2005,2020),
    "0600023":(2014,2020),
    "0600025":(2018,2020),
    "0600026":(2003,2020),
    "0600027":(2005,2020),
    "0600028":(2002,2020),
    "0600029":(2004,2020),
    "0600030":(2003,2020),
    "0600031":(2004,2020),
    "0600033":(2002,2020),
    "0600035":(2005,2020),
    "0600036":(2003,2020),
    "0600037":(2001,2020),
}

if __name__ == "__main__":
    snn = Stock_LSTM(input_size=6, hidden_size=128, num_layers=1, hidden_linear=32)
    train(snn, ALL_DATA, None, epoch =50, lr = 0.002, save_path = "./net/NN")
    # sample(torch.load("./net/NN"), id = "0600000", year=2003)