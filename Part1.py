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
    if block is None or block.id in visited:
        return
    visited.add(block.id)
    if block.statements:
        blocks.append(block)
    for exit_edge in block.exits:
        collect_blocks(exit_edge.target, visited, blocks)


def main(filename):
    cfg = CFGBuilder().build_from_file("program", filename)

    blocks = []
    collect_blocks(cfg.entryblock, set(), blocks)

    # Sort by starting line for more stable output
    def start_line(b):
        return min(getattr(s, "lineno", 0) for s in b.statements) if b.statements else 0

    blocks.sort(key=start_line)

    print(f"# of nodes = {len(blocks)}")

    for block in blocks:
        if not block.statements:
            continue
        first = min(getattr(s, "lineno", 0) for s in block.statements)
        last = max(getattr(s, "end_lineno", getattr(s, "lineno", 0)) for s in block.statements)
        print()
        print(f"NODE {block.id}: line {first} - {last}")
        for stmt in block.statements:
            print(unparse(stmt))

    # Collect edges
    edges = []
    for block in blocks:
        for edge in block.exits:
            if edge.target is None:
                continue
            cond = unparse(edge.exitcase)
            edges.append((block.id, edge.target.id, cond))

    print()
    print(f"# of edges = {len(edges)}")
    for src, dst, cond in edges:
        if cond:
            print(f"EDGE: node {src} -> node {dst}, when ({cond})")
        else:
            print(f"EDGE: node {src} -> node {dst}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Part1.py <program.py>")
        sys.exit(1)
    main(sys.argv[1])
