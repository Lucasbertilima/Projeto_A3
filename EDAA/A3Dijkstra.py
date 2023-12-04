import matplotlib.pyplot as plt
import networkx as nx


point_coord = []
edges = []
with open("distancias_cidades.txt", "r") as f:
    for line in f:
        split_line = line.split(';')
        edges.append((split_line[0], split_line[1], {'peso': int(split_line[2])}))
        for point in split_line[:2]:
            point_coord.append(point)

nodes = list(set(point_coord))


def project():
    options = int(input(
        f'\n1 - Dijkstra (Menor distância entre dois pontos)\n2 - Criar Pilha\n3 - Criar Fila\n4 - Sair\n'
        f'Com base nas opções, o que deseja realizar: '))

    if options == 1:
        first_choice = str(input(f"\nDigite o ponto de saída com relação aos seguintes nós - {nodes}: "))
        second_choice = str(input("Agora, sendo diferente do ponto de saída, digite o ponto de destino: "))

        if (first_choice == second_choice) or (first_choice not in nodes) or (second_choice not in nodes):
            print(f"Algum dos elementos indicados não consta nos nós: {nodes}, ou são iguais")
        else:
            G = nx.Graph()

            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            ccm = nx.dijkstra_path(G, source=first_choice, target=second_choice)
            weight_ccm = []
            weight_total = 0

            for i_ccm in range(0, (len(ccm) - 1)):
                for edge in edges:
                    if (((ccm[i_ccm] + ccm[(i_ccm + 1)]) in ''.join(edge[:2])) or
                            ((ccm[(i_ccm + 1)] + ccm[i_ccm]) in ''.join(edge[:2]))):
                        weight_ccm.append(edge)

            for weight_cost in weight_ccm:
                weight_total += weight_cost[2]['peso']

            print('\n-----------------------------------------------------------\nCaminho de custo mínimo: ', ccm)
            print('Peso(s) entre cada aresta do caminho de custo mínimo: ', weight_ccm)
            print('Tamanho do caminho de custo mínimo: ', weight_total)

            weight = nx.get_edge_attributes(G, 'peso')  # Atribui os "pesos" a arestas.

            # pos = nx.circular_layout(G)  # Posiciona os vértices
            pos = nx.spring_layout(G)  # Posiciona os vértices

            nx.draw_networkx(G, pos, node_size=200)  # Estipula o tamanho das vértices

            nx.draw_networkx_labels(G, pos)  # Colocar os números nos vertices

            nx.draw_networkx_edges(G, pos)  # Faz a criação das arestas

            nx.draw_networkx_edge_labels(G, pos, edge_labels=weight, label_pos=0.5)  # Coloca a legenda dos pesos

            plt.show()  # Mostra o gráfico

        project()

    elif options == 2:
        print("\nCriação da pilha:\n")
        for edge in reversed(edges):
            print(edge)

        project()

    elif options == 3:
        print("\nCriação da fila:\n")
        for edge in edges:
            print(edge)

        project()

    else:
        print("\nSaindo...")


project()
