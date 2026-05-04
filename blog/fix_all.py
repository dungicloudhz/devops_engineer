import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find missing </div> for sb-progress
    pattern = re.compile(r'(<div class="sb-progress">\s*<div class="sb-progress-label">.*?</div>\s*<div class="sb-progress-bar"><div class="sb-progress-fill"[^>]*></div></div>)\s*<div class="sb-section">\s*<div class="sb-section-label">📚 Series DevOps</div>', re.DOTALL)
    
    if pattern.search(content):
        print(f"Fixing missing div in {filepath}")
        content = pattern.sub(r'\1\n  </div>\n\n  <div class="sb-section">\n    <div class="sb-section-label">📚 Series DevOps</div>', content)
        
        # Remove the extra </div> pushed down
        content = content.replace('  </div>\n  </div>\n\n  <div class="sb-section">', '  </div>\n\n  <div class="sb-section">')
        content = content.replace('  </div>\n  </div>\n\n  <div class="sb-footer">', '  </div>\n\n  <div class="sb-footer">')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
