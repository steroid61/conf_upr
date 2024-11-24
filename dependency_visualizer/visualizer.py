import os
import argparse
from datetime import datetime, timezone, timedelta
from typing import Dict, List


class GitObject:
    """Class representing a Git object."""

    def __init__(self, sha1: str, obj_type: str, content: bytes):
        self.sha1 = sha1
        self.type = obj_type
        self.content = content.decode('utf-8', errors='replace')


class CommitNode:
    """Class representing a commit in the dependency graph."""

    def __init__(self, sha1: str, author: str, parents: List[str], files: List[str]):
        self.sha1 = sha1
        self.author = author
        self.parents = parents
        self.files = files


def parse_config(config_path, repo_path, output_path, file_name) -> Dict[str, str]:
    """
    Returns:
        A dictionary with configuration parameters.
    """
    config = {
        'graphviz_path': config_path,
        'repo_path': repo_path,
        'output_path': output_path,
        'file_name': file_name,
    }
    return config


def read_object(repo_path: str, sha1: str) -> GitObject:
    """
    Reads a Git object from the repository using git cat-file.

    Args:
        repo_path: Path to the Git repository.
        sha1: SHA1 hash of the object.

    Returns:
        A GitObject instance.
    """
    import subprocess

    result = subprocess.run(
        ['git', 'cat-file', '-p', sha1],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise FileNotFoundError(f"Object '{sha1}' not found.")

    # Determine the type of the object
    type_result = subprocess.run(
        ['git', 'cat-file', '-t', sha1],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    obj_type = type_result.stdout.strip()

    return GitObject(sha1, obj_type, result.stdout.encode('utf-8'))


def parse_commit(obj: GitObject, repo_path: str) -> CommitNode:
    """
    Parses a Git commit object.

    Args:
        obj: GitObject instance representing a commit.

    Returns:
        A CommitNode instance.:
    """
    from git import Repo
    lines = obj.content.split('\n')
    parents = []
    author = ''
    for line in lines:
        if line.startswith('parent '):
            parents.append(line[7:])
        elif line.startswith('author '):
            author_info = line[7:]
            # Разбиваем строку на части
            # Формат: "Имя <email> timestamp timezone"
            author_parts = author_info.rsplit(' ', 2)
            author_name_email = author_parts[0]
            author = author_name_email

    commit_sha = obj.sha1
    commit = Repo(repo_path).commit(commit_sha)
    files = [f for f in commit.stats.files.keys()]
    return CommitNode(obj.sha1, author, parents, files)


def build_commit_graph(repo_path: str, file_name: str) -> Dict[str, CommitNode]:
    """
    Builds the commit graph starting from a specific commit.

    Args:
        repo_path: Path to the Git repository.
        file_name: File name.

    Returns:
        A dictionary mapping commits SHA1 to CommitNode.
    """
    from git import Repo
    repo = Repo(repo_path)
    commits_sha1 = []
    for commit in repo.iter_commits():
        if file_name in commit.stats.files:
            commits_sha1.append(commit.hexsha)

    graph = {}
    for commit_sh1 in commits_sha1:
        obj = read_object(repo_path, commit_sh1)
        commit_node = parse_commit(obj, repo_path)
        graph[commit_sh1] = commit_node
    return graph


def generate_dot(graph: Dict[str, CommitNode]) -> str:
    """
    Generates a DOT representation of the commit graph.

    Args:
        graph: The commit graph.

    Returns:
        A string containing the DOT graph.
    """
    dot = 'digraph G {\n'
    dot += '  rankdir=LR;\n'
    dot += '  node [shape=box, style=filled, color="lightblue"];\n'  # Добавлены стили для узлов
    dot += '  edge [color="gray"];\n'  # Добавлены стили для ребер

    for sha1, node in graph.items():
        label = f"{node.sha1[:7]}\\n{node.author}\\n Files: {', '.join(node.files)}"
        dot += f'  "{sha1}" [label="{label}"];\n'
        for parent_sha1 in node.parents:
            if parent_sha1 in graph:
                dot += f'  "{sha1}" -> "{parent_sha1}";\n'
    dot += '}\n'
    return dot


def write_dot_file(dot_content: str, dot_path: str) -> None:
    """
    Writes the DOT content to a file.

    Args:
        dot_content: The DOT graph content.
        dot_path: Path to the output DOT file.
    """
    with open(dot_path, 'w') as f:
        f.write(dot_content)


def generate_graph_image(graphviz_path: str, dot_path: str, output_path: str, layout: str = 'dot') -> None:
    """
    Generates the graph image using Graphviz.

    Args:
        graphviz_path: Path to the Graphviz executable.
        dot_path: Path to the DOT file.
        output_path: Path to the output image file.
        layout: Graphviz layout engine to use.
    """
    import subprocess
    subprocess.run([graphviz_path, '-K', layout, '-Tpng', dot_path, '-o', output_path], check=True)


def main(args) -> None:
    """
    Main function to execute the visualization process.

    Args:
        args: all arguments.
    """
    # Parse configuration
    config = parse_config(args.graphviz_path, args.repo_path, args.output_path, args.file_name)
    # Build commit graph
    graph = build_commit_graph(config['repo_path'], config["file_name"])

    # Generate DOT file
    dot_content = generate_dot(graph)
    dot_path = os.path.join(os.path.dirname(config['output_path']), 'graph.dot')
    write_dot_file(dot_content, dot_path)

    # Generate graph image
    generate_graph_image(config['graphviz_path'], dot_path, config['output_path'])

    print("Graph generated successfully.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Git Commit Dependency Graph Visualizer')
    parser.add_argument('graphviz_path', help='Path to the graphviz output file')
    parser.add_argument('repo_path', help='Path to the repository')
    parser.add_argument('output_path', help='Path to the output file')
    parser.add_argument('file_name', help='File name')
    args = parser.parse_args()
    main(args)
