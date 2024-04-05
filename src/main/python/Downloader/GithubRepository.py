import os
import stat
import shutil

from git import Repo
from Compiler import Compiler


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
        self.folder = destination_folder + "\\" + split_name[0] + "\\" + split_name[1] + "\\Source"
        self.branch_name = branch_name

    def download_repository(self):
        if os.path.isdir(self.folder):
            if not os.listdir(self.folder):
                print("Directory is empty, downloading...")
                print("Repository: " + self.repository_url)
                if self.branch_name == "":
                    Repo.clone_from(self.repository_url, self.folder)
                else:
                    Repo.clone_from(self.repository_url, self.folder, branch=self.branch_name)
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
                    Repo.clone_from(self.repository_url, self.folder)
                except:
                    pass
            else:
                try:
                    Repo.clone_from(self.repository_url, self.folder, branch=self.branch_name)
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
                    os.removedirs(directory + "\\" + dir)
                else:
                    self.delete_file_unused(directory + "\\" + dir)
        else:
            if not directory.endswith(".py"):
                os.remove(directory)

    def compile_repository_files(self):
        print("Compiling all files")
        Compiler.compile_repository_files(self.folder)
        print("Successfully Compiled!")

    def delete_reporitory(self):
        print("Deleting Repository")
        shutil.rmtree(self.folder)
        print("Successfully Deleted!")
