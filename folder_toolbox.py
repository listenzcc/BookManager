# %% Importing
# System
from pprint import pprint
import os

# Collection
from collections import defaultdict

# Settings
TARGET_FOLDER = os.path.join('files',
                             'inventory')

# %% Defs


class FolderNode(dict):
    def __init__(self,
                 basename,
                 fullpath,
                 depth,
                 description='',
                 num_folders=0,
                 num_files=0):
        super(FolderNode, self).__init__()

        # Basic settings
        self.basename = basename
        self.fullpath = fullpath
        self.depth = depth

        # Contains
        self.folders = []
        self.files = []

        # Optional settings
        self.description = description
        self.num_folders = num_folders
        self.num_files = num_files

    def attr2key(self):
        self['basename'] = self.basename
        self['fullpath'] = self.fullpath
        self['depth'] = self.depth
        self['folders'] = self.folders
        # self['files'] = self.files
        self['description'] = self.description
        self['num_folders'] = self.num_folders
        self['num_files'] = self.num_files

    def add_folder(self, node):
        # Legal assert
        assert(type(node) == type(self))
        assert(node.depth - self.depth == 1)

        # Append
        self.folders.append(node)
        self.num_folders += 1

    def add_file(self, filename):
        # Legal assert
        try:
            assert(os.path.exists(os.path.join(self.fullpath, filename)))
            assert(os.path.isfile(os.path.join(self.fullpath, filename)))
        except AssertionError:
            raise AssertionError(
                f'Wrong path: {os.path.join(self.fullpath, filename)}')

        # Append
        self.files.append(filename)
        self.num_files += 1

    def brief(self):
        return dict(baseline=self.basename,
                    fullpath=self.fullpath,
                    depth=self.depth,
                    description=self.description,
                    num_dir=self.num_dir,
                    num_file=self.num_file)

    # def __str__(self):
    #     return '{}'.format(self.brief())


class FileTree():
    def __init__(self, root, max_depth=-1):
        # Legal assert
        assert(self.is_dir(root))

        # Settings
        self.root = root
        node = FolderNode(basename='.',
                          fullpath=root,
                          depth=0)
        self.node = node
        self.max_depth = max_depth

        self.listdir(root, self.node)

    def is_dir(self, path):
        # Return if path is a legal directory
        basename = os.path.basename(path)
        if basename.startswith('.'):
            return None

        return os.path.isdir(path)

    def is_under_max_depth(self, depth):
        # Return if path is under max_depth
        if self.max_depth < 0:
            return True

        return depth < self.max_depth

    def listdir(self, dirpath, node):
        # Legal assert
        assert(self.is_dir(dirpath))

        # Get current depth
        depth = node.depth
        assert(type(depth) == type(0))

        # Report
        print(f'Working in {dirpath}, depth is {depth}')

        if not self.is_under_max_depth(depth):
            return 1

        # Check every node in dirpath
        for childname in os.listdir(dirpath):
            # Get fullpath of the childname
            fullpath = os.path.join(dirpath, childname)

            # Seperat operation for ignore, dir and file
            is_dir = self.is_dir(fullpath)

            if is_dir is None:
                # Ignore
                continue

            if is_dir:
                # Dir opeartion
                _node = FolderNode(basename=childname,
                                   fullpath=fullpath,
                                   depth=depth+1)
                node.add_folder(_node)
                self.listdir(fullpath, _node)
            else:
                # File operation
                node.add_file(childname)

        node.attr2key()


# %%
if __name__ == '__main__':
    filetree = FileTree(TARGET_FOLDER)
    pprint(filetree.node)
