import requests
import matplotlib.pyplot as plt
import sys

def draw_k_line(id, year="2020"):

    url = "http://img1.money.126.net/data/hs/kline/day/history/"+year+"/"+id+".json"
    r = requests.get(url)
    response_dict = r.json()

    num = len(response_dict["data"])

    fig = plt.figure(figsize=(min(num/5, 17),5))
    ax = fig.add_subplot(111, axisbg="black")
    ax.set_xlim(0, num)

    all_lowest = 100000000
    all_highest = 0
    idx_lowest = 0
    idx_highest = 0
    for i in range(num):
        day = response_dict["data"][i]
        start = day[1]
        end = day[2]
        highest = day[3]
        lowest = day[4]
        
        if lowest < all_lowest:
            all_lowest = lowest
            idx_lowest = i
        if highest > all_highest:
            all_highest = highest
            idx_highest = i
        if start < end: # red line
            rect = plt.Rectangle((i,start),0.75, end - start, color="red")
            ax.add_patch(rect)
            line = plt.Line2D((i+0.4,i+0.4),(lowest,highest), color="red")
            ax.add_line(line)
        else: # black line
            rect = plt.Rectangle((i,end),0.75, start - end, color="green")
            ax.add_patch(rect)
            line = plt.Line2D((i+0.4,i+0.4),(lowest,highest), color="green")
            ax.add_line(line)

    text=plt.Text(idx_lowest,all_lowest-(all_highest-all_lowest)/12,'%.2f'%all_lowest, color="yellow", fontsize=10)
    ax.add_artist(text)
    text=plt.Text(idx_highest,all_highest+(all_highest-all_lowest)/20,'%.2f'%all_highest, color="cyan", fontsize=10)
    ax.add_artist(text)

    ax.set_ylim(all_lowest - (all_highest-all_lowest)/5, all_highest + (all_highest-all_lowest)/5)

    plt.grid(axis="y",linestyle='--', color='grey')
    plt.title(response_dict["symbol"]+"/"+year)
    plt.show()
    print(response_dict["name"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        #print("usage: python draw_k_line.py year id")
        draw_k_line("0000001", "2020")
        draw_k_line("0600536", "2020")
        draw_k_line("0601009", "2020")
    else:
        draw_k_line(sys.argv[2], sys.argv[1])
