from py2cfg import CFGBuilder
import ast
import sys


def unparse(node):
    if node is None:
        return None

    try:
        return ast.unparse(node)
    except Exception:
        return str(node)


def collect_blocks(block, visited, blocks):
    if block.id in visited:
        return

    visited.add(block.id)
    blocks.append(block)

    for exit_edge in block.exits:
        collect_blocks(exit_edge.target, visited, blocks)


def main(filename):
    print("FILE BEING ANALYZED:", filename)
    cfg = CFGBuilder().build_from_file("program", filename)

    blocks = []
    collect_blocks(cfg.entryblock, set(), blocks)

    real_blocks = [b for b in blocks if b.statements]

    print(f"# of nodes = {len(real_blocks)}")

    for block in sorted(real_blocks, key=lambda b: b.id):

        first_line = min(
            getattr(stmt, "lineno", 0)
            for stmt in block.statements
        )

        last_line = max(
            getattr(stmt, "end_lineno",
                   getattr(stmt, "lineno", 0))
            for stmt in block.statements
        )

        print()
        print(
            f"NODE {block.id}: line "
            f"{first_line} - {last_line}"
        )

        for stmt in block.statements:
            print(unparse(stmt))

    edges = []

    for block in real_blocks:

        for edge in block.exits:

            if edge.target is None:
                continue

            condition = unparse(edge.exitcase)

            edges.append(
                (block.id, edge.target.id, condition)
            )

    print()
    print(f"# of edges = {len(edges)}")

    for src, dst, cond in edges:

        if cond:
            print(
                f"EDGE: node {src} -> "
                f"node {dst}, when ({cond})"
            )
        else:
            print(
                f"EDGE: node {src} -> node {dst}"
            )


if __name__ == "__main__":
    main(sys.argv[1])