import sys
import numpy as np

def perf_stats_summary(file_path):
    rps = []
    clks = []
    with open(file_path) as f:
        perf_stats = f.readlines()
        for line in perf_stats:
            stats = line.split(';')[1][1:-3].split(',')
            rps.append(float(stats[0]))
            clks.append(float(stats[1]))
    rps = np.array(rps)
    clks = np.array(clks)
    rp_mean = np.mean(rps);rp_sd = np.std(rps)
    clk_mean = np.mean(clks);clk_sd = np.std(clks)
    print("        Mean            SD")
    print("rprec:  {0} {1}".format(rp_mean,rp_sd))
    print("click: {0} {1}".format(clk_mean,clk_sd))

if __name__ == '__main__':
    try:
        perf_stats_summary(sys.argv[1])
    except:
        print("Usage: python perf_summary.py file_path")
