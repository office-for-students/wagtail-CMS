import sys


def bump_version(level):
    with open('../version.txt', 'r') as file:
        version = file.read().replace('\n', '')

    version_parts = version.split('.')

    if len(version_parts) != 3:
        print('invalid')
    else:
        if level == 'major':
            version_parts[0] = str(int(version_parts[0]) + 1)
        elif level == 'minor':
            version_parts[1] = str(int(version_parts[1]) + 1)
        elif level == 'patch':
            version_parts[2] = str(int(version_parts[2]) + 1)
        new_version = '.'.join(version_parts)
        with open('../version.txt', 'w') as file:
            file.write(new_version)
        print(new_version)


if __name__ == '__main__':
    bump_version(*sys.argv[1:])
