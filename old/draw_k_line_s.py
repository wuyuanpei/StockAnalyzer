from draw_k_line import draw_k_line
import sys

# 使用本地数据画k线图
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python draw_k_line_s.py year id")
    else:
        draw_k_line(sys.argv[2], sys.argv[1], "./data")