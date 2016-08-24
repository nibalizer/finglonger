import sys
import yaml


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        snippet = yaml.load(f.read())
    print snippet['task']['shell']

