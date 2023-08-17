import pkg_resources
def get_library_versions(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    libraries = []
    for line in lines:
        if line.startswith('import') or line.startswith('from'):
            parts = line.split()
            if len(parts) >= 2:
                library = parts[1]
                libraries.append(library)

    versions = {}
    for library in libraries:
        try:
            version = pkg_resources.get_distribution(library).version
            versions[library] = version
        except pkg_resources.DistributionNotFound:
            versions[library] = 'Not installed'

    return versions

library_versions = get_library_versions('app.py')
for library, version in library_versions.items():
    print(f'{library}: {version}')