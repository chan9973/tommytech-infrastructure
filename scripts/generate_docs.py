#!/usr/bin/env python3
"""
LLM-Wiki Documentation Generator
Generates architecture diagrams, decision logs, and cross-reference maps from your vault.

Usage: python generate_docs.py --type <diagram|decision-log|xref|all> [topic]
       python generate_docs.py --help
"""

import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional

# Vault root path
VAULT_SUMMARY = r"E:/tommy vault/tommy vault/Read & Write"


class WikiGraph:
    """Build and query the wikilink knowledge graph"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.nodes: Dict[str, dict] = {}
        self.edges: List[Tuple[str, str, str]] = []
        self._build_graph()
    
    def _build_graph(self):
        """Walk the vault and build a wikilink graph"""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                node_id = md_file.stem
                tags = self._extract_tags(content)
                wikilinks = self._extract_wikilinks(content, node_id)
                
                self.nodes[node_id] = {
                    'path': str(md_file),
                    'title': node_id,
                    'tags': tags,
                    'wikilinks': wikilinks
                }
                
                for link in wikilinks:
                    self.edges.append((node_id, link, 'link'))
            except Exception:
                continue
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract YAML frontmatter tags"""
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            tags_match = re.search(r'tags:\s*\[(.*?)\]', match.group(1))
            if tags_match:
                return [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]
        return []
    
    def _extract_wikilinks(self, content: str, source_id: str) -> Set[str]:
        """Extract all [[wikilinks]] from content"""
        links = set()
        for match in re.finditer(r'\[\[([^\]|#]+)', content):
            link_text = match.group(1).split(']')[0].strip()
            if link_text and link_text != source_id:
                normalized = link_text.lower().replace(' ', '-')
                links.add(normalized)
        return links


def generate_architecture_diagram(graph: WikiGraph, output_path: Optional[str] = None) -> str:
    """Generate Mermaid architecture diagram from vault structure"""
    
    domains = {}
    for node_id, node_data in graph.nodes.items():
        path = Path(node_data['path'])
        try:
            parts = path.parts
            vault_idx = next(i for i, p in enumerate(parts) if 'Read & Write' in p or 'Read&Write' in p.lower())
            if vault_idx + 2 < len(parts):
                domain = parts[vault_idx + 2]
            else:
                domain = 'memories'
        except (StopIteration, IndexError):
            domain = 'memories'
        
        if domain not in domains:
            domains[domain] = {'nodes': [], 'tags': set()}
        domains[domain]['nodes'].append(node_id)
        domains[domain]['tags'].update(node_data['tags'])
    
    # Build mermaid diagram
    lines = [
        "%% LLM-Wiki Architecture Diagram",
        f"%% Generated: {datetime.now().isoformat()}",
        "",
        "```mermaid",
        "graph TD",
        "    subgraph Core[Core Infrastructure]",
        "        hermes[Hermes Agent] -->|reads| obsidian[Obsidian Vault]",
        "        obsidian -->|writes| inbox[Inbox/]",
        "        obsidian -->|reads| scripts[scripts/]",
        "    end",
        "",
        "    subgraph Domains[Knowledge Domains]"
    ]
    
    for domain, data in sorted(domains.items()):
        node_refs = []
        for node in data['nodes'][:5]:
            clean_name = node.replace(' ', '-')
            node_refs.append(f'    {clean_name}["[[{node}]]"]')
        
        if node_refs:
            domain_label = domain.replace('-', ' ').title()
            lines.append(f'        subgraph {domain.replace(" ", "_")}["{domain_label}"]')
            lines.append('            ' + ' --> '.join(node_refs[:3]))
            lines.append('        end')
    
    lines.extend([
        "    end",
        "",
        "    classDef domain fill:#F5F5F5,stroke:#333,stroke-width:2px",
        "    classDef core fill:#E3F2FD,stroke:#1976D2,stroke-width:3px",
        "",
        "    class hermes,obsidian,inbox,scripts core",
        "```",
        "",
        "<!-- Tag Summary -->",
        f"Total domains: {len(domains)}",
        "<!-- Tags observed: " + ", ".join(sorted(set(t for d in domains.values() for t in d['tags']))) + " -->"
    ])
    
    diagram = "\n".join(lines)
    
    if output_path is None:
        output_path = str(Path(VAULT_SUMMARY) / "_wiki" / "architecture-diagram.md")
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(diagram, encoding='utf-8')
    print(f"✓ Architecture diagram saved to: {output_path}")
    
    return diagram


def generate_decision_log(graph: WikiGraph, topic: Optional[str] = None) -> str:
    """Generate decision log from notes with status tags"""
    
    decisions = []
    
    for node_id, node_data in graph.nodes.items():
        tags = node_data['tags']
        if any(s in [t.lower() for t in tags] for s in ['production', 'pending', 'active', 'deprecated']):
            content = Path(node_data['path']).read_text(encoding='utf-8')
            
            decision = {
                'topic': node_id.replace('-', ' ').title(),
                'status': next((t for t in tags if t.lower() in ['production', 'pending', 'active', 'deprecated']), 'unknown'),
                'wikilink': f"[[Read & Write/{node_id}]]",
                'tags': tags
            }
            decisions.append(decision)
    
    lines = [
        "---",
        f"tags: [decision-log, documentation, {datetime.now().strftime('%Y-%m')}]",
        f"generated: {datetime.now().isoformat()}",
        "---",
        "",
        f"# Decision Log [[memories/decision-log-{datetime.now().strftime('%Y%m%d')}]]",
        "",
        "> Curated decisions from your LLM-Wiki vault. Each entry links to original documentation.",
        "",
        "## Active Decisions",
        ""
    ]
    
    for d in sorted(decisions, key=lambda x: x['topic']):
        emoji_map = {'production': '✅', 'active': '✅', 'pending': '⏳', 'deprecated': '🚫'}
        status_emoji = emoji_map.get(d['status'], '📝')
        
        lines.extend([
            f"### {d['topic']} {status_emoji}",
            f"- **Status**: `{d['status']}`",
            f"- **Source**: {d['wikilink']}",
            f"- **Tags**: {', '.join(d['tags'][:5])}",
            ""
        ])
    
    return "\n".join(lines)


def generate_cross_reference_map(graph: WikiGraph, output_path: Optional[str] = None) -> Dict:
    """Generate comprehensive cross-reference analysis"""
    
    xref_map = {}
    
    for node_id, node_data in graph.nodes.items():
        inbound = [src for src, tgt, _ in graph.edges if tgt == node_id]
        outbound = list(node_data.get('wikilinks', []))
        
        linked_tags = []
        for linked in outbound[:10]:
            linked_data = graph.nodes.get(linked, {})
            linked_tags.extend([t for t in linked_data.get('tags', []) if t != 'web-source'])
        
        xref_map[node_id] = {
            'inbound_links': len(inbound),
            'outbound_links': len(outbound),
            'connected_tags': list(set(linked_tags)),
            'isolation_score': 0 if (len(inbound) > 0 or len(outbound) > 0) else 1
        }
    
    sorted_nodes = sorted(xref_map.items(), key=lambda x: -(x[1]['inbound_links'] + x[1]['outbound_links']))
    
    result = {
        'metadata': {
            'total_nodes': len(graph.nodes),
            'total_edges': len(graph.edges),
            'generated': datetime.now().isoformat()
        },
        'top_connected': sorted_nodes[:20],
        'isolated_nodes': [n for n, d in xref_map.items() if d['isolation_score']],
        'by_tags': {}
    }
    
    for node_id, node_data in graph.nodes.items():
        for tag in node_data.get('tags', []):
            if tag not in result['by_tags']:
                result['by_tags'][tag] = []
            result['by_tags'][tag].append(node_id)
    
    if output_path is None:
        output_path = str(Path(VAULT_SUMMARY) / "memories" / f"xref-map-{datetime.now().strftime('%Y%m%d')}.json")
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(f"✓ Cross-reference map saved to: {output_path}")
    
    return result


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h']:
        print("LLM-Wiki Documentation Generator")
        print("")
        print("Usage:")
        print("  python generate_docs.py --type <diagram|decision-log|xref|all> [topic]")
        print("  python generate_docs.py --help           # Show this help")
        print("")
        print("Examples:")
        print("  python generate_docs.py --type diagram")
        print("  python generate_docs.py --type decision-log qwen3.5")
        print("  python generate_docs.py --type all")
        sys.exit(0)
    
    cmd_type = sys.argv[1].replace('--type', '').strip()
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("Building knowledge graph...")
    graph = WikiGraph(VAULT_SUMMARY)
    print(f"Found {len(graph.nodes)} notes with {len(graph.edges)} links\n")
    
    if cmd_type in ['diagram', 'all']:
        print("=" * 60)
        print("GENERATED ARCHITECTURE DIAGRAM")
        print("=" * 60)
        diagram = generate_architecture_diagram(graph)
        print(diagram)
        print()
    
    if cmd_type in ['decision-log', 'all']:
        print("=" * 60)
        print("DECISION LOG")
        print("=" * 60)
        log = generate_decision_log(graph, topic)
        print(log)
        print()
    
    if cmd_type in ['xref', 'all']:
        print("=" * 60)
        print("CROSS-REFERENCE ANALYSIS")
        print("=" * 60)
        xref = generate_cross_reference_map(graph)
        print(f"\nMetadata:")
        print(f"  - Total notes: {xref['metadata']['total_nodes']}")
        print(f"  - Total links: {xref['metadata']['total_edges']}")
        print(f"  - Top connected notes: {len(xref['top_connected'])}")
        if xref['isolated_nodes']:
            print(f"  - Isolated notes: {', '.join(xref['isolated_nodes'][:5])}")
        print()


if __name__ == "__main__":
    main()