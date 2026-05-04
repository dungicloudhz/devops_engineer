import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to make sure sb-progress is properly closed.
    # If we see:
    #     <div class="sb-progress-fill" id="prog-fill"></div></div>
    # 
    #   <div class="sb-section">
    #     <div class="sb-section-label">📚 Series DevOps</div>
    # we know it's missing a closing </div> for sb-progress before sb-section.
    # And there is an extra </div> after sb-section or at the end.
    
    # Let's fix it by regex:
    # Find <div class="sb-progress"> ... <div class="sb-section">
    match = re.search(r'<div class="sb-progress">(.*?)<div class="sb-section">\s*<div class="sb-section-label">📚 Series DevOps</div>', content, re.DOTALL)
    if match:
        progress_content = match.group(1)
        if progress_content.count('<div') > progress_content.count('</div'):
            # Missing closing div
            print(f"Fixing {filepath}")
            # Add </div> before <div class="sb-section">
            content = content[:match.end(1)] + '  </div>\n\n' + content[match.end(1):]
            
            # Now we need to remove the extra </div> that got pushed down.
            # The extra </div> was originally right before <div class="sb-section"> (the next one).
            # Let's find the next sb-section or end of nav, and remove a stray </div> before it.
            
            # Wait, let's just find the closing </nav> and if there are too many </div>s, remove one.
            # Actually, it's safer to just replace the whole `<nav id="sidebar">...</nav>` with a properly parsed one, or just do a simple replacement.
            
