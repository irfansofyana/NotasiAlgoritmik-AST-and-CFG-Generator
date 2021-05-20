from graphviz import Digraph
from src.api.functions import *


def visualize_cfg(cfg, is_graphviz=False, output_path='test-output/result.gv'):
    if not is_graphviz:
        graph = convert_cfg_to_graphviz(cfg)
    else:
        graph = cfg
    graph.node_attr['fontname'] = 'consolas'
    graph.render(output_path, format='png', view=False)


def convert_cfg_to_graphviz(cfg):
    graph = Digraph(comment="CFG result")
    traverse_cfg(cfg, graph)
    return graph


def convert_cfg_json_to_graphviz(cfg_json):
    def merge_statements(statements):
        statements_str = ''
        for statement in statements:
            if statements_str == '':
                statements_str += statement
            else:
                statements_str += f'\n{statement}'
        return statements_str

    graph = Digraph(comment="CFG result")
    for node in cfg_json["nodes"]:
        graph.node(str(node['label']), str(merge_statements(node['statements'])))
    for edge in cfg_json["edges"]:
        graph.edge(str(edge['start_node_label']), str(edge['end_node_label']))

    return graph


def traverse_cfg(cfg, graph):
    for node in cfg:
        graph.node(str(node.get_label()), node.get_info_str())

    for node in cfg:
        for adj_node in cfg[node]:
            graph.edge(str(node.get_label()), str(adj_node.get_label()))


if __name__=="__main__":
    file_path = '../backend/parser/input/6.in'
    cfg = get_cfg(file_path)
    visualize_cfg(cfg)