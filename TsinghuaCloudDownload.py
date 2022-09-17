# coding=utf-8
import requests
import json
import os
import re

"""
MIT License

Copyright (c) 2020 zqthu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

class THUCloud():
    def __init__(self, shared_link, outdir=None):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"}
        
        if "/f/" in shared_link: # single file
            print("This is a single file.")
            self.is_dir = False
            self.is_lib = False
            archive = shared_link.split("/f/")[-1].split("/")[0]
            print(f"Id is: {archive}")
            self.api_link = "https://cloud.tsinghua.edu.cn/f/{}/".format(archive)
            self.file_link = "https://cloud.tsinghua.edu.cn/f/{}/?dl=1".format(archive)
        elif '/d/' in shared_link: # dir
            print("This is a directory.")
            self.is_dir = True
            self.is_lib = False
            archive = shared_link.split("/d/")[-1].split("/")[0]
            print(f"Id is: {archive}")
            if shared_link.find("?p=") != -1:
                self.path = shared_link.split("?p=")[-1].split("&mode=list")[0]
            else:
                self.path = "/"
            print("Path is: {}".format(self.path.replace("%2F", "/")))
            self.api_link = "https://cloud.tsinghua.edu.cn/api/v2.1/share-links/{}/dirents/".format(archive)
            self.file_link = "https://cloud.tsinghua.edu.cn/d/{}/files/".format(archive)
        elif '/library/' in shared_link: # lib
            print("This is a library directory.")
            self.is_dir = True
            self.is_lib = True
            with open("Cookie.txt", "r") as f:
                cookie = f.read()
            self.headers["Cookie"] = cookie
            archive = shared_link.split("/library/")[-1].split("/")[0]
            self.path = shared_link.split(archive)[-1].split("/")
            self.path.pop(1)
            self.path = "%2F".join(self.path)
            print("Path is: {}".format(self.path.replace("%2F", "/")))
            self.api_link = "https://cloud.tsinghua.edu.cn/api/v2.1/repos/{}/dir/".format(archive)
            self.file_link = "https://cloud.tsinghua.edu.cn/lib/{}/file".format(archive)
        else:
            raise ValueError("Cannot parse the shared link.")
        print("api_link is: {}".format(self.api_link))
        print("file_link is: {}".format(self.file_link))

        if outdir is None:
            self.current_dir = os.getcwd()
        else:
            self.current_dir = os.path.abspath(outdir)
        if not os.path.exists(self.current_dir):
            os.mkdir(self.current_dir)   
        
    def _move_to(self, to_dir):
        self.current_dir = os.path.abspath(os.path.join(self.current_dir, to_dir))
        # print(self.current_dir)
        if not os.path.exists(self.current_dir):
            os.mkdir(self.current_dir)        

    def _parse_url(self, path):
        if self.is_lib == False:
            url = self.api_link + '?path=' + path
        else:
            url = self.api_link + '?p=' + path + "&with_thumbnail=true"
        response = requests.get(url=url, headers=self.headers)
        assert response.status_code == 200
        return response.content.decode()

    def _retrieve_file(self, url, name): # for small files
        file_path = os.path.join(self.current_dir, name)
        print("Current file is: {}".format(name))
        response = requests.get(url=url, headers=self.headers)
        assert response.status_code == 200
        content = response.content
        with open(file_path, "wb") as f:
            f.write(content)
        print("Downloaded: {}\n".format(file_path))

    def _recursion_download(self, path):
        response = self._parse_url(path)
        response_dict = json.loads(response)
        for item in response_dict['dirent_list']:
            # print(item)
            if self.is_lib == False:
                if item['is_dir'] == True:
                    next_path = item['folder_path']
                    self._move_to(item['folder_name'])
                    print(f"***********************************\nCurrent dir is: {self.current_dir}")
                    self._recursion_download(next_path)
                else:
                    url = self.file_link + '?p=' + item['file_path'] + '&dl=1'
                    self._retrieve_file(url, item['file_name'])
            else:
                if item['type'] == "dir":
                    next_path = item['parent_dir'] + item["name"]
                    self._move_to(item['name'])
                    print(f"***********************************\nCurrent dir is: {self.current_dir}")
                    self._recursion_download(next_path)
                else:
                    url = self.file_link + item['parent_dir'] + item["name"] + '&dl=1'
                    self._retrieve_file(url, item['name'])
        self._move_to("..")
    
    def download(self):
        if self.is_dir:
            self._recursion_download(self.path) # initial data, default download all files
        else:
            response = requests.get(url=self.api_link, headers=self.headers)
            assert response.status_code == 200
            content = response.content.decode()
            name = re.search(r"fileName: '(.*)',", content).group(1)
            self._retrieve_file(self.file_link, name)

if __name__ == "__main__":
    introduction = """
    This is a script to download files from Tsinghua Cloud.
    Based on Github project of zqthu. link: https://github.com/zqthu/thu_cloud_download
    可下载他人共享的清华云盘链接或者自己的资料库中的所有文件，只要输入需要下载的链接即可。
    注意：如果是下载资料库中的文件，需要先登录清华云盘，然后将Cookie.txt中的内容替换为自己的Cookie。
    查找自己的Cookie的方法可自行上网搜索。
    """

    example = """
    Examples of shared link:
        https://cloud.tsinghua.edu.cn/f/2c50c14239b641d09633/
        https://cloud.tsinghua.edu.cn/d/dd37da8463504030aec9/
        https://cloud.tsinghua.edu.cn/d/dd37da8463504030aec9/?p=%2F07-14%20Git&mode=list
        https://cloud.tsinghua.edu.cn/library/deae987a-d50b-4827-8e77-1263437145bd/%E8%BF%90%E5%8A%A8%E5%B0%8F%E5%88%86%E9%98%9F/
    """

    # replace the shared_link here
    shared_link = input(f"{introduction} {example} Please input the shared link: ")

    # output dir (optional)
    out_dir = "Download"
    t = THUCloud(shared_link, out_dir)
    t.download()

    print("***********************************\nDownload Complete!")
    s = input("请按任意字符退出...")