#!/usr/bin/env python3
"""
Obsidian to Digital Garden Jekyll Sync Script
Converts Obsidian notes to digital garden format with proper titles and navigation
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
import argparse

class ObsidianDigitalGardenSync:
    def __init__(self, obsidian_path, jekyll_path):
        self.obsidian_path = Path(obsidian_path)
        self.jekyll_path = Path(jekyll_path)
        self.notes_dir = self.jekyll_path / "_notes"
        self.assets_dir = self.jekyll_path / "assets"
        
        # Ensure directories exist
        self.notes_dir.mkdir(exist_ok=True)
        (self.assets_dir / "images").mkdir(parents=True, exist_ok=True)
        
    def sync_all_notes(self):
        """Sync all publishable notes from Obsidian to Jekyll"""
        print("🔄 Starting Obsidian to Digital Garden sync...")
        
        # Find all markdown files in Obsidian vault
        obsidian_notes_dir = self.obsidian_path / "Notes"
        if not obsidian_notes_dir.exists():
            print(f"❌ Obsidian notes directory not found: {obsidian_notes_dir}")
            return
            
        processed_count = 0
        skipped_count = 0
        
        for md_file in obsidian_notes_dir.glob("*.md"):
            try:
                if self.process_note(md_file):
                    processed_count += 1
                    print(f"✅ Processed: {md_file.name}")
                else:
                    skipped_count += 1
                    print(f"⏭️  Skipped: {md_file.name}")
            except Exception as e:
                print(f"❌ Error processing {md_file.name}: {e}")
                
        print(f"\n🎉 Sync complete! Processed: {processed_count}, Skipped: {skipped_count}")
        
    def process_note(self, note_file):
        """Process a single Obsidian note"""
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse frontmatter and content
        frontmatter, body = self.parse_frontmatter(content)
        
        # Skip if not marked for publishing
        if not frontmatter.get('publish', True):  # Default to publish
            return False
            
        # Convert filename to slug
        slug = self.filename_to_slug(note_file.stem)
        
        # Process content for digital garden
        processed_body = self.process_content(body, note_file.parent)
        
        # Enhance frontmatter for digital garden
        enhanced_frontmatter = self.create_digital_garden_frontmatter(
            frontmatter, slug, note_file.stem
        )
        
        # Write to Jekyll _notes directory
        output_file = self.notes_dir / f"{slug}.md"
        self.write_jekyll_note(output_file, enhanced_frontmatter, processed_body)
        
        return True
        
    def parse_frontmatter(self, content):
        """Extract YAML frontmatter and content body"""
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                    return frontmatter, body
            except yaml.YAMLError:
                pass
        return {}, content
        
    def filename_to_slug(self, filename):
        """Convert filename to URL-friendly slug"""
        # Remove common prefixes like "My Daily Planning System" -> "daily-planning-system"
        slug = filename.lower()
        slug = re.sub(r'^(my|the|a|an)\s+', '', slug)
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
        
    def process_content(self, content, source_dir):
        """Process Obsidian content for digital garden"""
        # Convert Obsidian wikilinks [[Note Name]] to Jekyll format
        content = re.sub(
            r'\[\[([^\]|]+)(\|([^\]]+))?\]\]',
            lambda m: self.convert_wikilink(m.group(1), m.group(3)),
            content
        )
        
        # Process image links ![[image.jpg]]
        content = re.sub(
            r'!\[\[([^\]]+\.(jpg|jpeg|png|gif|webp|svg))\]\]',
            lambda m: self.process_image(m.group(1), source_dir),
            content
        )
        
        # Convert Obsidian callouts to digital garden format
        content = self.convert_callouts(content)
        
        return content
        
    def convert_wikilink(self, link_target, link_text=None):
        """Convert Obsidian wikilink to digital garden format"""
        # Create slug from link target
        slug = self.filename_to_slug(link_target)
        display_text = link_text or link_target
        
        # Digital garden uses [[note-slug]] format
        return f"[[{slug}|{display_text}]]"
        
    def process_image(self, image_name, source_dir):
        """Process and copy images"""
        # Look for image in Obsidian attachments
        attachment_dirs = [
            self.obsidian_path / "98-Attachments",
            self.obsidian_path / "attachments",
            source_dir,  # Same directory as note
        ]
        
        source_file = None
        for att_dir in attachment_dirs:
            potential_path = att_dir / image_name
            if potential_path.exists():
                source_file = potential_path
                break
                
        if source_file:
            # Copy to Jekyll assets
            dest_file = self.assets_dir / "images" / image_name
            shutil.copy2(source_file, dest_file)
            return f"![{image_name}](/assets/images/{image_name})"
        
        return f"![{image_name}](missing-image.jpg)"
        
    def convert_callouts(self, content):
        """Convert Obsidian callouts to HTML"""
        callout_pattern = r'^> \[!(\w+)\](.*)$'
        lines = content.split('\n')
        result_lines = []
        in_callout = False
        callout_type = None
        
        for line in lines:
            callout_match = re.match(callout_pattern, line)
            if callout_match:
                if in_callout:
                    result_lines.append('</div>')
                callout_type = callout_match.group(1).lower()
                callout_title = callout_match.group(2).strip()
                result_lines.append(f'<div class="callout callout-{callout_type}">')
                if callout_title:
                    result_lines.append(f'<div class="callout-title">{callout_title}</div>')
                in_callout = True
            elif in_callout and line.startswith('> '):
                result_lines.append(line[2:])  # Remove "> " prefix
            elif in_callout and not line.strip():
                result_lines.append('')
            else:
                if in_callout:
                    result_lines.append('</div>')
                    in_callout = False
                result_lines.append(line)
                
        if in_callout:
            result_lines.append('</div>')
            
        return '\n'.join(result_lines)
        
    def create_digital_garden_frontmatter(self, original_fm, slug, original_filename):
        """Create enhanced frontmatter for digital garden"""
        fm = {
            'title': original_fm.get('title', original_filename),
            'slug': slug,
            'last_modified_at': datetime.now().isoformat(),
        }
        
        # Copy over relevant fields
        for field in ['date', 'tags', 'description', 'nav_title']:
            if field in original_fm:
                fm[field] = original_fm[field]
                
        # Add digital garden specific fields
        fm['layout'] = 'note'
        
        # Set nav_title for cleaner navigation
        if 'nav_title' not in fm and 'title' in fm:
            title = fm['title']
            # Create shorter nav title
            if len(title) > 30:
                # Try to shorten intelligently
                shortened = re.sub(r'^(My|The|A|An)\s+', '', title)
                shortened = re.sub(r'\s*[-:]\s*.*$', '', shortened)  # Remove subtitles
                fm['nav_title'] = shortened if len(shortened) < len(title) else title
            else:
                fm['nav_title'] = title
                
        return fm
        
    def write_jekyll_note(self, output_file, frontmatter, content):
        """Write processed note to Jekyll _notes directory"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
            f.write('---\n\n')
            f.write(content)

    def sync_home_page(self):
    """Sync the Home.md from Obsidian vault to Jekyll index"""
    home_file = self.obsidian_path / "Home.md"
    if home_file.exists():
        with open(home_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter and content
        frontmatter, body = self.parse_frontmatter(content)
        
        # Convert Obsidian links to Jekyll format
        body = re.sub(
            r'\[\[Notes/([^|]+)\|([^\]]+)\]\]',
            lambda m: f"[[{self.filename_to_slug(m.group(1))}|{m.group(2)}]]",
            body
        )
        
        # Handle images
        body = re.sub(
            r'!\[\[([^\]]+)\]\]',
            lambda m: f"![{m.group(1)}]({{{{ '/assets/images/{m.group(1)}' | relative_url }}}})",
            body
        )
        
        # Create Jekyll homepage
        jekyll_frontmatter = {
            'layout': 'page',
            'title': frontmatter.get('title', 'Jonathan Nguyen'),
            'id': 'home',
            'permalink': '/'
        }
        
        # Write to _pages/index.md
        pages_dir = self.jekyll_path / "_pages"
        pages_dir.mkdir(exist_ok=True)
        
        with open(pages_dir / "index.md", 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(jekyll_frontmatter, f, default_flow_style=False, allow_unicode=True)
            f.write('---\n\n')
            f.write(body)
            f.write('\n\n<style>\n  .wrapper {\n    max-width: 46em;\n  }\n</style>')
        
        print("✅ Synced homepage from Obsidian vault")

def main():
    parser = argparse.ArgumentParser(description='Sync Obsidian notes to Digital Garden Jekyll')
    parser.add_argument('--obsidian-path', 
                       default='/Users/jonathan/Obsidian/jonathannguyen.net',
                       help='Path to Obsidian vault')
    parser.add_argument('--jekyll-path',
                       default='/Users/jonathan/GitHub/personal/jonathannguyen-net-jekyll',
                       help='Path to Jekyll site')
    
    args = parser.parse_args()
    
    syncer = ObsidianDigitalGardenSync(args.obsidian_path, args.jekyll_path)
    syncer.sync_home_page()  # Sync homepage from Obsidian
    syncer.sync_all_notes()  # Sync all notes

if __name__ == "__main__":
    main()