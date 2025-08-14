from pyhocon import ConfigFactory

def config_man(name_input: str):
    """
    Read the hocon file for the input.
    :param name_input: input name for the file.
    :return: config of the job.
    """

    # Ensure the config file is read correctly, handling BOM if present
    with open(name_input, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("\ufeff"):
        content = content[1:]

    return ConfigFactory.parse_string(content).get('Velespro')