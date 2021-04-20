# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

'''
Energy consumption = Power(kW)*Time(h)
'''

def sigmoid(z):
    return -7/(1+np.exp((0.005)*(-z+200)))+80


def bell_curve(x, mu, sigma):
    # import pdb; pdb.set_trace()
    r_ = np.exp(-(x-mu)**2/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
    return r_

class STATE_GRAPH():
    """docstring for STATE_GRAPH.
        Building a possible working state graph for each request
    """

    def __init__(self, start_temp, time_limit, target_temp, temp_time_gear_relation, power_gear_level):
        super(STATE_GRAPH, self).__init__()
        self.start_temp = start_temp
        self.time_limit = time_limit
        self.target_temp = target_temp
        self.n_level = temp_time_gear_relation.shape[1] - 1
        self.temp_time_gear_relation = temp_time_gear_relation
        self.power_gear_level = power_gear_level

        self.layer = self.start_temp - self.target_temp + 1

        self.graph = self.build_graph()


    def build_graph(self):

        graph = {}
        for i in np.arange(self.layer):
            for j in np.arange((self.n_level)):
                # import pdb; pdb.set_trace()
                # weights = self.weight_calculation(f'node_{i}_{j}', np.arange(self.n_level*(j+1)-self.n_level, self.n_level*(j+1)))
                if i == 0 and j != 0:
                    continue
                weights = self.weight_calculation(f'node_{i}_{j}', np.arange(self.n_level))

                if i == np.arange(self.layer)[-1]:
                    graph.update({f'node_{i}_{j}':[]})
                else:
                    graph.update({f'node_{i}_{j}':weights})

            # print(graph)
            # import pdb; pdb.set_trace()
        return graph


    def weight_calculation(self, root_node, sub_node_arr):
        # import pdb; pdb.set_trace()
        temp = root_node.split('_')[1]
        num_gear_level = root_node.split('_')[2]
        weight_list = {}
        for sub_node in sub_node_arr:
            cur_gear_level = sub_node % 3
            # print(sub_node)
            # import pdb; pdb.set_trace()
            time_s = np.where(np.round(self.temp_time_gear_relation[:,3 - cur_gear_level]) == (self.start_temp - float(temp)))[0][0]
            time_e = np.mean(np.where(np.round(self.temp_time_gear_relation[:,3 - cur_gear_level]) == (self.start_temp - float(temp) - 1))[0])
            time_consum = time_e - time_s
            # import pdb; pdb.set_trace()
            # time_e - time_s
            energy_consum = np.mean(self.power_gear_level[:,cur_gear_level+1]) * time_consum/60
            # import pdb; pdb.set_trace()
            weight = time_consum + energy_consum # loss as weight, combining time and energy consumption
            # weight = energy_consum # loss as weight, combining time and energy consumption

            # print(weight)
            weight_list.update({f'node_{int(temp)+1}_{sub_node}':weight})

            # print(weight_list)

            # import pdb; pdb.set_trace()
        # self.temp_time_gear_relation[1]
        return weight_list


    def optimize_path_finder(self):
        pass


def main(start_temp: int, target_temp: int):
    """

    :param start_temp:
    :param target_temp:
    :return:
    """

    #### make data for Temp and Time given different gear level 0, 1, 2, 3

    time_temp_list = np.arange(-70,70)
    show_time_list = time_temp_list[:70]
    vars()[f'temp_time_gear_0'] = np.ones_like(time_temp_list[:70]) * 80
    # TODO: A big problem is why the temp drop will stop at 73.
    std_list = [13,19,30]
    for ind, std in enumerate(std_list):

        raw_curve = bell_curve(time_temp_list,0,std)
        vars()[f'temp_time_gear_{ind+1}'] = (7* raw_curve/max(raw_curve)+ 73)[70:]


    for jnd in range(4):
        vars()[f'temp_time_gear_{jnd}'] = np.random.rand(70)*0.4 + vars()[f'temp_time_gear_{jnd}']
        plt.plot(vars()[f'temp_time_gear_{jnd}'],'-*',label=f'Gear {jnd}')
    plt.legend()


    #### make data for energy consumption
    E_list = [0,17,22,25]
    vars()[f'power_gear_0'] = np.ones_like(show_time_list) * E_list[0]
    vars()[f'power_gear_1'] = np.ones_like(show_time_list) * E_list[1] + np.random.rand(70)*0.3
    vars()[f'power_gear_2'] = np.ones_like(show_time_list) * E_list[2] + np.random.rand(70)*0.3
    vars()[f'power_gear_3'] = np.ones_like(show_time_list) * E_list[3] + np.random.rand(70)*0.3



    plt.figure()
    plt.plot(time_temp_list[70:], vars()[f'power_gear_0'], '-x', label='Gear 0')
    plt.plot(time_temp_list[70:], vars()[f'power_gear_1'], '-x', label='Gear 1')
    plt.plot(time_temp_list[70:], vars()[f'power_gear_2'], '-x', label='Gear 2')
    plt.plot(time_temp_list[70:], vars()[f'power_gear_3'], '-x', label='Gear 3')


    plt.legend()
    # plt.show()

    # import pdb; pdb.set_trace()
    temp_time_gear_arr = np.concatenate((vars()[f'temp_time_gear_0'][:,np.newaxis],
                                            vars()[f'temp_time_gear_1'][:,np.newaxis],
                                            vars()[f'temp_time_gear_2'][:,np.newaxis],
                                            vars()[f'temp_time_gear_3'][:,np.newaxis]),1)
    power_gear_arr = np.concatenate((vars()[f'power_gear_0'][:,np.newaxis],
                                        vars()[f'power_gear_1'][:,np.newaxis],
                                        vars()[f'power_gear_2'][:,np.newaxis],
                                        vars()[f'power_gear_3'][:,np.newaxis]),1)

    # start_temp = 80
    # target_temp = 76

    graph_ob = STATE_GRAPH(start_temp=start_temp, time_limit=80, target_temp=target_temp, temp_time_gear_relation=temp_time_gear_arr, power_gear_level=power_gear_arr)
    graph = graph_ob.build_graph()
    # import pdb; pdb.set_trace()

    def Dijkstra(G,v0,INF=999):
        book = set()
        minv = v0
        dis = dict((k,INF) for k in G.keys())
        dis[v0] = 0
        path = []

        path_result = {}
        while len(book)<len(G):
            # print(len(book))
            # print(len(G))
            book.add(minv)
            # path.append(minv)
            for w in G[minv]:
                if dis[minv] + G[minv][w] < dis[w]:
                    dis[w] = dis[minv] + G[minv][w]
                    path.append([minv,w])
                    # path.update({minv:[w]})
                    path_result.update({w:path})
                    # import pdb; pdb.set_trace()
            new =INF
            for v in dis.keys():
                if v in book:
                    continue
                if dis[v] < new:
                    new = dis[v]
                    minv = v

        # import pdb; pdb.set_trace()
        return dis

    dis = Dijkstra(graph, 'node_0_0')
    keys = dis.keys()
    dist_5 = []
    for k in keys:
        if k.split('_')[1] == str(start_temp-target_temp):
            dist_5.append(dis[k])
        # dist_5.append(dis[k])
    lowest_cost_node = f'node_{str(start_temp-target_temp)}_{(np.where(np.array(dist_5) == min(dist_5)))[0][0]}'
    # import pdb; pdb.set_trace()

    G = nx.DiGraph()
    for key in graph.keys():
        if len(graph[key]) == 0:
            continue
        for subkey in graph[key].keys():
            G.add_weighted_edges_from([(key, subkey, graph[key][subkey])])
    predecessors, _ = nx.floyd_warshall_predecessor_and_distance(G)
    #print(nx.reconstruct_path("node_0_0", lowest_cost_node, predecessors))

    opt = nx.reconstruct_path("node_0_0", lowest_cost_node, predecessors)
    x, y, z = opt[-1].split('_')
    print(z)
    # import pdb; pdb.set_trace()
    dis = Dijkstra(graph, 'node_0_0')
    # import pdb; pdb.set_trace()

    keys = dis.keys()
    dist_5 = []
    for k in keys:
        # if k.split('_')[1] == '5':
        #     dist_5.append(dis[k])
        dist_5.append(dis[k])
    plt.figure()
    plt.plot(dist_5, '-x')
    plt.show()

    #import pdb; pdb.set_trace()

    # points = list(range(0, len(time_temp_list)-1200))
    # value = time_temp_list[1200:]
    # x = np.linspace(0, len(time_temp_list)-1200, num=2*(len(time_temp_list)-1200))
    # # import pdb; pdb.set_trace()
    # y = np.interp(x, points, value)
    # result_list = time_temp_list[:1200]+list(y)
    # # for i in range(5):
    # # result_list[1200] = (result_list[1199]+result_list[1201])/2
    #
    # noise_list = np.random.rand(len(result_list))*0.2
    #
    # result_list = np.array(result_list)+noise_list
    #
    # plt.plot(result_list)
    # plt.show()
    return z


if __name__ == '__main__':
    plan = main(start_temp=80, target_temp=76)
    #print(plan)
