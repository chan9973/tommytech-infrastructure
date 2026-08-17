#!/usr/bin/env python3
"""
Wiki Ingestion Test Suite - Run to test all ingestion sources
python wiki_ingest_test.py [url or text]
"""

import sys
import os

# Import the actual script functions (adjust import path based on your setup)
sys.path.insert(0, r"E:/tommy vault/tommy vault/Read & Write/.hermes/scripts")

from wiki_ingest import process_ingest

def test_url():
    """Test 1: Ingest from URL"""
    print("=== TEST 1: Ingest from URL ===")
    try:
        # Use a safe demo URL (this will redirect properly)
        url = "https://news.ycombinator.com/item?id=40862579"
        path = process_ingest(url)
        print(f"✓ Success! Created: {path}\n")
    except Exception as e:
        print(f"⚠ URL test skipped (network): {e}\n")

def test_raw_text():
    """Test 2: Ingest raw text"""
    print("=== TEST 2: Ingest Raw Text ===")
    text = "This is a demo research note about machine learning concepts. " \
           "Machine learning algorithms like neural networks learn patterns from data. " \
           "Key concepts include training, validation, and inference phases."
    
    try:
        path = process_ingest(text)
        print(f"✓ Success! Created: {path}\n")
    except Exception as e:
        print(f"⚠ Text test error: {e}\n")

def test_markdown_file():
    """Test 3: Ingest from markdown file"""
    print("=== TEST 3: Ingest from Markdown File ===")
    
    # Create a sample markdown file if it doesn't exist
    sample_dir = r"E:/tommy vault/tommy vault/Read & Write/.hermes/scripts"
    sample_file = os.path.join(sample_dir, "research-notes.md")
    
    try:
        sample_content = """---
created: 2026-08-15T11:00:00+08:00
source-url: https://notes.example.com/research
tags: [machine-learning, research]
---

# Research Notes: Neural Network Basics

Core concepts covered:
1. **Training** - optimizing model parameters via gradient descent
2. **Validation** - checking generalization on held-out data  
3. **Inference** - running predictions on new inputs

These notes are part of my research collection on [[machine-learning]]."""
        
        # Write sample file
        os.makedirs(sample_dir, exist_ok=True)
        with open(sample_file, 'w') as f:
            f.write(sample_content)
        
        print(f"  Created sample: {sample_file}\n")
        
        # Now ingest it as a URL to demo the process
        path = process_ingest(sample_file)
        print(f"✓ Success! Ingested: {path}\n")
    except Exception as e:
        print(f"⚠ File test error: {e}\n")

def main():
    """Run all tests"""
    print("🧪 Wiki Ingestion Test Suite\n" + "="*50)
    
    # Run each test
    test_url()
    test_raw_text()
    test_markdown_file()
    
    # Show results
    print("="*50)
    print("\n📋 Summary of Created Files:")
    
    import glob
    vault_path = r"E:/tommy vault/tommy vault/Read & Write"
    for i, file in enumerate(glob.glob(os.path.join(vault_path, "**/*.md", recursive=False)), 1):
        if ".hermes/" in str(file) and "SKILL.md" not in str(file) and "README.md" not in str(file):
            try:
                with open(file) as f:
                    title = f.readline().strip() or "[Untitled]"
                print(f"  {i}. [{file}] - {title}")
            except:
                print(f"  {i}. [{file}]")

if __name__ == "__main__":
    main()
