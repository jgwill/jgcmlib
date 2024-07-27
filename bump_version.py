import re

def bump_version(version):
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    return f"{major}.{minor}.{patch}"

with open('setup.py', 'r') as file:
    setup_content = file.read()

version_match = re.search(r"version=['\"]([^'\"]*)['\"]", setup_content)
if version_match:
    current_version = version_match.group(1)
    new_version = bump_version(current_version)
    new_setup_content = re.sub(r"version=['\"]([^'\"]*)['\"]", f"version='{new_version}'", setup_content)

    with open('setup.py', 'w') as file:
        file.write(new_setup_content)

    print(new_version)
else:
    raise ValueError("Version string not found in setup.py")