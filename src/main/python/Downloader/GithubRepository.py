import os
import stat
import shutil

from git import Repo
from Compiler import Compiler
from Downloader.ProgressionCheck import Progress


class GithubRepository:
    repository_name = ""
    destination_folder = ""
    repository_url = ""
    branch_name = ""
    folder = ""

    def __init__(self, repository_name, destination_folder, branch_name):
        self.repository_name = repository_name
        self.destination_folder = destination_folder
        self.repository_url = "https://github.com/" + repository_name
        split_name = repository_name.split("/")
        self.folder = os.path.join(destination_folder, split_name[0], split_name[1], "Source")
        self.branch_name = branch_name

    def download_repository(self):
        if os.path.isdir(self.folder):
            if not os.listdir(self.folder):
                print("Directory is empty, downloading...")
                print("Repository: " + self.repository_url)
                if self.branch_name == "":
                    Repo.clone_from(self.repository_url, self.folder, progress=Progress())
                else:
                    Repo.clone_from(self.repository_url, self.folder, branch=self.branch_name,
                                    progress=Progress())
                print("Repository Downloaded!")
            else:
                print("Directory is not empty")
                print(self.folder)
                print("Please delete it or use DownloadGithub.delete_repository method")
        else:
            print("Directory not exist, downloading...")
            print("Repository: " + self.repository_url)
            if self.branch_name == "":
                try:
                    Repo.clone_from(self.repository_url, self.folder, progress=Progress())
                except:
                    pass
            else:
                try:
                    Repo.clone_from(self.repository_url, self.folder, branch=self.branch_name,
                                    progress=Progress())
                except:
                    pass
            print("Repository Downloaded!")

    def change_permissions(self):
        print("Changing all permissions of repository files")
        for root, dirs, files in os.walk(self.folder):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)
        print("Permissions Successfully Changed!")

    def delete_files_unused(self):
        print("Deleting all unused files")
        self.delete_file_unused(self.folder)
        print("Successfully Deleted!")

    def delete_file_unused(self, directory):
        if os.path.isdir(directory):
            for dir in os.listdir(directory):
                if not os.listdir(self.folder):
                    os.removedirs(os.path.join(directory, dir))
                else:
                    self.delete_file_unused(os.path.join(directory, dir))
        else:
            if not directory.endswith(".py"):
                try:
                    os.remove(directory)
                except:
                    pass

    def delete_empty_folder(self, directory):
        if os.path.isdir(directory):
            list_dir = os.listdir(directory)
            if list_dir.__len__() == 0:
                os.removedirs(directory)
            else:
                for dir in list_dir:
                    if not os.listdir(self.folder):
                        os.removedirs(os.path.join(directory, dir))
                    else:
                        self.delete_empty_folder(os.path.join(directory, dir))

    def delete_folders_unused(self):
        print("Deleting all empty folders")
        self.delete_empty_folder(self.folder)
        print("Successfully Deleted!")

    def compile_repository_files(self, terminal):
        print("Compiling all files")
        Compiler.compile_repository_files(self.folder, terminal)
        print("Successfully Compiled!")

    def delete_repository(self):
        print("Deleting Repository")
        try:
            shutil.rmtree(os.path.join(self.destination_folder, self.repository_name))
        except FileNotFoundError:
            pass
        print("Successfully Deleted!")
