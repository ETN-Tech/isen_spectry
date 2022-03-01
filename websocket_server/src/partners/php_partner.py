import requests
from requests.exceptions import RequestException

class PhpPartner():
    def __init__(self, base_url, state=None) -> None:
        self.base_url = base_url
        self.state = state or False

        if state == None:
            self.state = self._get("probe")[0]


    def copy_partner(self):
        return PhpPartner(base_url=self.base_url, state=self.state)


    def _call(self, method_callback, endpoint, print_=False, get_code=False):
        print("php - call", endpoint)
        try:
            result = method_callback()
        except RequestException:
            raise Exception("php - server not started")

        if print_:
            print(f"php - status_code {result.status_code}")
            print("php - content")
            print(result.content.decode("utf-8"))
            print("php - finish")

        return result.status_code if get_code else result.status_code == 200, result.content.decode("utf-8")


    def _get(self, endpoint, print_=False, get_code=False):
        return self._call(lambda: requests.get(url=f"{self.base_url}?action={endpoint}"), endpoint, print_, get_code)


    def _post(self, endpoint, data, print_=False, get_code=False):
        return self._call(lambda: requests.post(url=f"{self.base_url}?action={endpoint}", data=data), endpoint, print_, get_code)


    def set_project_folder(self, project_name):
        if not self.state:
            return False

        return self._post("create_folder", { "project_name": project_name })[0]


    def set_project_files(self, project_name, files):
        if not self.state:
            return False

        print("upload all files")

        for file in files:
            data = { 
                "project_name": project_name,
                "file_name": file['name'],
                "file_content": file['content']
            }
            if not self._post("create_file", data)[0]:
                return False

        print("finish all files")

        return True


    def unset_project_files(self, project_name):
        if not self.state:
            return False

        return self._post("remove_files", { "project_name": project_name })[0]


    def unset_project_folder(self, project_name):
        if not self.state:
            return False

        return self._post("remove_folder", { "project_name": project_name })[0]


    def get_project_page(self, project_name, page):
        if not self.state:
            return False

        data = {
            "project_name": project_name,
            "page": page
        }
        return self._post("execute", data, get_code=True)
