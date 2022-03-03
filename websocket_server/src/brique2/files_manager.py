import os

COLLECTION_PROJECTS = "projects"

class FilesManager():
    def __init__(self, partners, project_name) -> None:
        self.partners = partners
        self.project_name = project_name
        self.files_currently_stored = True

        filter_q = {
            "name": self.project_name
        }
        fields = {
            "_id": 0,
            "id": {
                "$toString": "$_id"
            },
        }
        self.project_id = self.partners["db"].find_one(COLLECTION_PROJECTS, filter_q, fields)["id"]
        if not self.project_id:
            raise Exception("FilesGenerator - __init__: unknow project name")

        self.files = self.partners["storage"].download_files_from_folder(self.project_id)

        if not self.partners["renderer"].set_project_folder(self.project_name):
            raise Exception(f"{self.project_name} - PHP - folder not created")

        # tmp secure
        if not self.partners["renderer"].unset_project_files(self.project_name):
            raise Exception(f"{self.project_name} - PHP - folder emptiness pb")

        if not self.partners["renderer"].set_project_files(self.project_name, self.files):
            raise Exception(f"{self.project_name} - PHP - files not uploaded")


    def _test(self):
        self.partners["storage"].upload_files_to_folder(self.project_id, [
            {
                "name": "test1.py",
                "content": "# !/usr/bin/python3 \n\ndef print_sorted(liste):\n    return sorted(liste)\n\n1"
            },
            {
                "name": "test2.py",
                "content": "# !/usr/bin/python3 \n\ndef print_sorted(liste):\n    return sorted(liste)\n\n2"
            },
            {
                "name": "test3.py",
                "content": "# !/usr/bin/python3 \n\ndef print_sorted(liste):\n    return sorted(liste)\n\n3"
            },
        ])

        self.files = self.partners["storage"].download_files_from_folder(self.project_id)
        print(self.files) # => working proof

        self.files = self.partners["storage"].upload_files_to_folder(self.project_id, []) # add in rest server for cleaning deleting projects


    def close(self):
        result = self.partners["renderer"].unset_project_files(self.project_name)
        print(f"{self.project_name} - PHP - Project files {'well' if result else 'not'} removed")
        if result is False:
            return
        result = self.partners["renderer"].unset_project_folder(self.project_name)
        print(f"{self.project_name} - PHP - Project directory {'well' if result else 'not'} removed")


    async def generate_files(self, specs_json):
        filepath = f"/src/brique2/cpp/{self.project_name}.json"
        open(filepath, "w").write(specs_json)
        args = (filepath,)

        lines, retcode = await self.partners["generator"].call(args)

        if os.path.exists(filepath):
            os.remove(filepath)

        if retcode == -1:
            return False

        chunks = lines.split("\n\n\n\n")

        if chunks[-1].split("\n")[0] == "error":  # retcode and retcode != 0:  # execution error
            print(f"cpp executable return error '{retcode}'")
            print(lines)
            return False

        self.files = [{"name": line.split("\n")[0], "content": line[line.find("\n")+1:]} for line in chunks][:-1]
        self.files_currently_stored = False
        print(self.files)

        return True


    def update_stored_files(self):
        if self.files_currently_stored:
            print(f"{self.project_name} - Project files already stored")
            return True

        result = self.partners["storage"].upload_files_to_folder(self.project_id, self.files)
        if not result:
            print(f"{self.project_name} - Project upload to storage failed")
            return False

        result = self.partners["renderer"].unset_project_files(self.project_name) # use id when ready
        if not result:
            print(f"{self.project_name} - Project upload to renderer step1/2 failed")
            return False

        result = self.partners["renderer"].set_project_files(self.project_name, self.files) # use id when ready
        if not result:
            print(f"{self.project_name} - Project upload to renderer step2/2 failed")
            return False

        self.files_currently_stored = True
        return True