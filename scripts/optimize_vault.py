#!/usr/bin/env python3
"""
Vault Optimization Script
- Detects and removes duplicate notes
- Suggests wikilink improvements
- Generates quality metrics for your LLM-Wiki
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, List, Tuple

VAULT_SUMMARY = r"E:\tommy vault\tommy vault\Read & Write"


class VaultOptimizer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.notes: Dict[str, dict] = {}
        self._load_notes()
    
    def _load_notes(self):
        """Load all markdown files with their content"""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                rel_path = md_file.relative_to(self.vault_path)
                self.notes[str(rel_path)] = {
                    'path': str(md_file),
                    'content': content,
                    'lines': len(content.split('\n')),
                    'chars': len(content),
                    'headers': self._extract_headers(content),
                    'wikilinks': set(re.findall(r'\[\[([^\]|#]+)', content)),
                    'tags': self._extract_tags(content)
                }
            except Exception:
                continue
    
    def _extract_headers(self, content: str) -> List[str]:
        """Extract all headers"""
        return re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from YAML frontmatter"""
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            tags_match = re.search(r'tags:\s*\[(.*?)\]', match.group(1))
            if tags_match:
                return [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]
        return []
    
    def find_duplicates(self, threshold: float = 0.85) -> List[Tuple[str, str, float]]:
        """Find potential duplicate notes based on content similarity"""
        duplicates = []
        note_paths = list(self.notes.keys())
        
        for i, path1 in enumerate(note_paths):
            for path2 in note_paths[i+1:]:
                content1 = self.notes[path1]['content']
                content2 = self.notes[path2]['content']
                
                similarity = SequenceMatcher(None, content1, content2).ratio()
                if similarity > threshold:
                    duplicates.append((path1, path2, similarity))
        
        return duplicates
    
    def find_orphaned_wikilinks(self) -> Dict[str, List[str]]:
        """Find wikilinks that point to non-existent notes"""
        all_targets = set()
        for node_data in self.notes.values():
            all_targets.update(node_data['wikilinks'])
        
        valid_paths = set(self.notes.keys())
        valid_names = {Path(p).stem for p in valid_paths}
        
        orphans = {}
        for source, node_data in self.notes.items():
            for link in node_data['wikilinks']:
                normalized = link.lower().replace(' ', '-')
                if normalized not in valid_names and link not in all_targets:
                    if source not in orphans:
                        orphans[source] = []
                    orphans[source].append(link)
        
        return orphans
    
    def generate_quality_report(self) -> dict:
        """Generate quality metrics for the vault"""
        total_notes = len(self.notes)
        total_chars = sum(n['chars'] for n in self.notes.values())
        total_links = sum(len(n['wikilinks']) for n in self.notes.values())
        
        tag_distribution = {}
        for note_data in self.notes.values():
            for tag in note_data['tags']:
                tag_distribution[tag] = tag_distribution.get(tag, 0) + 1
        
        # Calculate average notes per tag
        avg_per_tag = total_notes / max(len(tag_distribution), 1)
        
        return {
            'total_notes': total_notes,
            'total_characters': total_chars,
            'total_wikilinks': total_links,
            'links_per_note': total_links / max(total_notes, 1),
            'total_tags': len(tag_distribution),
            'avg_notes_per_tag': avg_per_tag,
            'most_used_tags': sorted(tag_distribution.items(), key=lambda x: -x[1])[:10],
            'duplicate_count': len(self.find_duplicates()),
            'orphan_count': sum(len(v) for v in self.find_orphaned_wikilinks().values())
        }
    
    def suggest_improvements(self) -> List[str]:
        """Suggest improvements to enhance vault quality"""
        suggestions = []
        report = self.generate_quality_report()
        
        if report['orphan_count'] > 0:
            suggestions.append(f"🔗 Found {report['orphan_count']} broken wikilinks - consider creating missing notes or fixing references")
        
        if report['duplicate_count'] > 0:
            suggestions.append(f"🔄 Found {report['duplicate_count']} potential duplicates - review for consolidation")
        
        if report['links_per_note'] < 2:
            suggestions.append("🔗 Low connectivity - add more wikilinks between related notes")
        
        if report['avg_notes_per_tag'] > 20:
            suggestions.append("🏷️ Tag '" + report['most_used_tags'][0][0] + "' has " 
                             f"{report['most_used_tags'][0][1]} notes - consider splitting into subcategories")
        
        return suggestions
    
    def run_analysis(self) -> str:
        """Run full analysis and return formatted report"""
        report = self.generate_quality_report()
        suggestions = self.suggest_improvements()
        
        lines = [
            "---",
            "tags: [vault-analysis, quality-report]",
            f"generated: {datetime.now().isoformat()}",
            "---",
            "",
            f"# Vault Quality Analysis [[memories/vault-quality-analysis-{datetime.now().strftime('%Y%m%d')}]]",
            "",
            "## Overview",
            "",
            f"- **Total Notes**: {report['total_notes']}",
            f"- **Total Characters**: {report['total_characters']:,}",
            f"- **Total Wikilinks**: {report['total_wikilinks']:,}",
            f"- **Average Links per Note**: {report['links_per_note']:.2f}",
            f"- **Tag Diversity**: {report['total_tags']} tags",
            "",
            "## Top Tags",
            ""
        ]
        
        for tag, count in report['most_used_tags'][:8]:
            lines.append(f"| `{tag}` | {count} notes |")
        
        lines.extend([
            "",
            "## Quality Metrics",
            "",
            f"- **Potential Duplicates**: {report['duplicate_count']}",
            f"- **Broken Links**: {report['orphan_count']}",
            ""
        ])
        
        if suggestions:
            lines.extend([
                "## Suggestions for Improvement",
                ""
            ] + suggestions)
        
        return "\n".join(lines)


if __name__ == "__main__":
    optimizer = VaultOptimizer(VAULT_SUMMARY)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--report':
        report = optimizer.run_analysis()
        print(report)
        
        # Save report
        output_path = Path(VAULT_SUMMARY) / "memories" / f"vault-quality-analysis-{datetime.now().strftime('%Y%m%d')}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
        print(f"\n✓ Report saved to: {output_path}")
    else:
        print("Vault Optimization Scripts")
        print("Usage:")
        print("  python optimize_vault.py --report   # Generate quality report")