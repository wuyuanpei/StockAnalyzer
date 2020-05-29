import matplotlib.pyplot as plt

plt.ion()

# 动态绘图器
class DynamicUpdate():
    # 构造绘图器
    # num_x:    所要画的点的个数
    # y_size:   所画点的区间为 0 ~ y_size
    #           如果y_size不声明, 图片的尺寸会动态加载
    def __init__(self, num_x, y_size = None):
        self.max_x = num_x
        self.max_y = y_size
        self.xdata = []
        self.ydata = []

    # 运行绘图器
    def on_launch(self):
        # Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'o')
        # Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(0, self.max_x)
        if self.max_y is not None:
            self.ax.set_ylim(0, self.max_y)
        # Other stuff
        self.ax.grid(axis='y')

    # 更新图片
    def on_running(self):
        # Update data (with the new _and_ the old points)
        self.lines.set_xdata(self.xdata)
        self.lines.set_ydata(self.ydata)
        # Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        # draw and flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    # 更新数据数组
    # y:        新的数据点
    # return:   目前为止的所有数据
    def draw(self, y):
        if not self.xdata:
            self.xdata.append(0)
        else:
            self.xdata.append(self.xdata[-1] + 1)
        self.ydata.append(y)
        self.on_running()
        return self.ydata


# # Example 
# import numpy as np
# import time
        
# d = DynamicUpdate(360, 100)
# d.on_launch()

# for y in np.arange(0,360):
#     res = d.draw(40 + np.random.randint(20) + 40 * np.sin(y * np.pi / 180))
#     time.sleep(0.01)

# print(res)
