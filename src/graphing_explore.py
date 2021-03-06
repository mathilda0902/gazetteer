from graphviz import Digraph
import json
import os
import logging


def view_source_dependency(source_file):

    with open(f'../maps/{source_file}', 'r') as f:
        view_source = json.load(f)
    
    return view_source


def gen_graph(explore_name, join_list, connection, view_source_payload):
    dot = Digraph(f'{explore_name}')
    dot.node(explore_name, explore_name)

    view_list = join_list

    for view in view_list:
    
        join_node = f'view_{view}'
        dot.node(join_node, join_node)
        dot.edge(explore_name, join_node, label=connection)

        try:
            with open(f'../maps/view-{view}.json', 'r') as f:
                payload = json.load(f)

                if payload['view_type'] == 'derived_table':
                    base_node = "Need further investigation"
                elif payload['view_type'] == 'extension':
                    base_node = view_source_payload[payload['view_name']]['base_view_name']
                else:
                    base_node = payload['source_table']
                
                dot.node(base_node, base_node)
                dot.edge(join_node, base_node)
        except:
            pass

    dot.render(f'../graphs/{explore_name}.gv', view=False)
    return logging.info(f'Successfully generated dependency graph for Explore {explore_name}.')


def main():

    for model_folder in next(os.walk(f'../maps'))[1]:
        for map_path in os.listdir(f'../maps/{model_folder}'):
            if map_path.startswith('explore-'):
                map_path = map_path.split('.')[0]

                logging.info(f"Generating dependency graph for explore {map_path}...")
                with open(f'../maps/{model_folder}/{map_path}.json', 'r') as f:
                    map_explore = json.load(f)

                    try:
                        view_source = view_source_dependency(f'{model_folder}/map-model-{model_folder}-{map_path}-source.json')
                        
                        gen_graph(explore_name=map_explore['explore_name'], join_list=map_explore['explore_joins'], \
                                    connection="", view_source_payload=view_source)

                    except:
                        pass

if __name__ == '__main__':

    main()
