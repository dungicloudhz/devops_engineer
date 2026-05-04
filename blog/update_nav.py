import os
import re

FILES = [
    ("terminal-macbook.html", "💻", "Terminal macOS"),
    ("linux-guide.html", "🐧", "Linux"),
    ("docker-guide.html", "🐳", "Docker"),
    ("aws-guide.html", "☁️", "AWS"),
    ("gcp-guide.html", "🌐", "GCP"),
    ("azure-guide.html", "🔷", "Azure"),
    ("teraform-guide.html", "🏗️", "Terraform"),
    ("kubernate-guide.html", "☸️", "Kubernetes"),
    ("gitlab-cicd-guide.html", "🦊", "GitLab CI/CD"),
    ("jenkins-guide.html", "👴", "Jenkins"),
    ("cicd-local-guide.html", "🏠", "CI/CD Local"),
    ("gitlab-cicd-k8s.html", "🦊", "GitLab CI/CD K8s"),
    ("jenkins-cicd-k8s.html", "👴", "Jenkins CI/CD K8s"),
    ("eks-cicd-guide.html", "🚀", "EKS · CI/CD · Lens"),
    ("cicd-springboot-react.html", "⚛️", "CI/CD Springboot React")
]

def generate_nav(template_type, current_file):
    if template_type == 'nav':
        lines = ['  <div class="nav-section">', '    <div class="nav-group-hdr ngh-5">📚 Series DevOps</div>']
        for f, icon, title in FILES:
            active = " active" if f == current_file else ""
            lines.append(f'    <a href="{f}" class="nav-link{active}"><span class="ico">{icon}</span> {title}</a>')
        lines.append('  </div>')
    else:
        lines = ['  <div class="sb-section">', '    <div class="sb-section-label">📚 Series DevOps</div>']
        for f, icon, title in FILES:
            active = " active" if f == current_file else ""
            lines.append(f'    <a class="sb-link{active}" href="{f}"><span class="sb-icon">{icon}</span>{title}</a>')
        lines.append('  </div>')
    return '\n'.join(lines)

def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine template type
    if 'class="nav-link"' in content or 'class="nav-link active"' in content or 'class="nav-section"' in content:
        template_type = 'nav'
    else:
        template_type = 'sb'

    new_section = generate_nav(template_type, filename)

    # Check if "Series DevOps" already exists
    pattern_existing = re.compile(r'  <div class="(?:nav-section|sb-section)">\s*<div class="(?:nav-group-hdr ngh-5|sb-section-label)">📚 Series DevOps</div>.*?</div>', re.DOTALL)
    
    if pattern_existing.search(content):
        content = pattern_existing.sub(new_section, content)
    else:
        # Inject it after the progress bar
        if template_type == 'nav':
            # Looking for: <div class="prog-wrap"><div class="prog-bar" id="pbar"></div></div>\n  </div>
            pattern_inject = re.compile(r'(<div class="prog-wrap">.*?</div>\s*</div>)', re.DOTALL)
            match = pattern_inject.search(content)
            if match:
                content = content[:match.end()] + '\n' + new_section + content[match.end():]
        else:
            # Looking for: <div class="sb-progress">...</div>
            pattern_inject = re.compile(r'(<div class="sb-progress">.*?</div>\s*</div>)', re.DOTALL)
            match = pattern_inject.search(content)
            if match:
                content = content[:match.end()] + '\n\n' + new_section + content[match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for html_file in [f[0] for f in FILES]:
    if os.path.exists(html_file):
        process_file(html_file)
        print(f"Processed {html_file}")
    else:
        print(f"Missing {html_file}")
