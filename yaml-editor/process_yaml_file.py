import yaml
from collections import OrderedDict


def read_yaml_file(file_path):
    """Read YAML file maintaining order"""

    # Custom loader to maintain order
    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping
    )

    try:
        with open(file_path, 'r') as file:
            data = yaml.load(file, Loader=OrderedLoader)
            if isinstance(data, dict):
                data = OrderedDict(data)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")


def write_yaml_file(data, file_path):
    """Write YAML file maintaining order"""

    # Custom dumper to maintain order
    class OrderedDumper(yaml.SafeDumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items()
        )

    OrderedDumper.add_representer(OrderedDict, _dict_representer)

    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file, Dumper=OrderedDumper, sort_keys=False)
        print(f"Successfully wrote to {file_path}")
    except Exception as e:
        print(f"Error writing YAML file: {e}")


def modify_yaml_keys(data):
    """Add -X to top-level keys"""
    modified_data = OrderedDict()
    for key in data:
        new_key = f"{key}-X"
        modified_data[new_key] = data[key]
    return modified_data


import json
# Example usage
if __name__ == "__main__":
    input_file = r"/yaml-editor/yaml_files/sample.yaml"
    output_file = r"/Users/paramraghavan/dev/utils/yaml-editor/yaml_files/sample-output.yaml"

    # Read
    yaml_data = read_yaml_file(input_file)
    json_str = json.dumps(yaml_data, indent=2)
    # Modify
    if yaml_data:
        modified_data = modify_yaml_keys(yaml_data)

        # Write
        write_yaml_file(modified_data, output_file)