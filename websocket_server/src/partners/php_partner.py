import requests
from requests.exceptions import RequestException

class PhpPartner():
    def __init__(self, base_url, state=None) -> None:
        self.base_url = base_url
        self.state = state or False

        if state == None:
            try:
                result = requests.get(url=f"{self.base_url}?action=probe")
            except RequestException:
                print("big exception") # serveur not started or bad url
            else:
                # print("status_code", result.status_code)
                self.state = result.status_code == 200


    def copy_partner(self):
        return PhpPartner(base_url=self.base_url, state=self.state)

    
    def set_project_folder(self, project_name):
        if not self.state:
            return False

        print("call to create_folder")
        try:
            result = requests.get(url=f"{self.base_url}?action=create_folder&project_name={project_name}")
        except RequestException:
            print("big exception") # serveur not started or bad url
            return False

        print("status_code", result.status_code)
        print("content\n________\n", result.content.decode("utf-8"))
        print("________\nfinish")

        return True

    
    def set_project_files(self, project_name, files):
        if not self.state:
            return False

        print("upload all files")

        for file in files:
            print("call to create_file")
            try:
                result = requests.get(url=f"{self.base_url}?action=create_file&project_name={project_name}&file_name={file['name']}&file_content={file['content']}")
            except RequestException:
                print("big exception") # serveur not started or bad url
                return False

            print("status_code", result.status_code)
            print("content\n________\n", result.content.decode("utf-8"))
            print("________\nfinish")

        print("finish all files")

        return True


    def unset_project_files(self, project_name):
        if not self.state:
            return False

        # try:
        #     result = requests.get(url=f"{self.base_url}?action=...")
        # except RequestException:
        #     print("big exception")
        #     return False

        return True


    def unset_project_folder(self, project_name):
        if not self.state:
            return False

        # try:
        #     result = requests.get(url=f"{self.base_url}?action=...")
        # except RequestException:
        #     print("big exception")
        #     return False

        return True


    def get_project_page(self, project_name, page):
        if not self.state:
            return False

        print("call to generate")
        try:
            result = requests.get(url=f"{self.base_url}?action=generate&project_name={project_name}&page={page}")
        except RequestException:
            print("big exception") # serveur not started or bad url
            return False

        print("status_code", result.status_code)
        print("content\n________\n", result.content.decode("utf-8"))
        print("________\nfinish")

        return True
