本项目基于项目https://github.com/zqthu/thu_cloud_download。

该项目的README文件如下：

# THU Cloud Download

## Usage

- Retrieve files from shared links of [Tsinghua Cloud][tsinghua_cloud].
- 从清华网盘的分享链接中批量下载文件

## How to Use It?

1. **Download** thu_cloud_download.py
2. **Type in** shared link
3. **Enjoy yourself~**

## License

[MIT][mit_licence]

## TODO

By now, this program can only download all files by default : )
More functions will be supported in the future:

- Download or block files in given list.
- Download or block files by the pattern of regular expression.



**本项目的附加信息：**

# 背景

众所周知，清华云盘是一个好用的云盘管理软件，然而当我们要从别人共享给我们的清华云盘链接中下载文件时，往往会得到 `size to large` 的警告信息，这就让我们不得不对目录中的每一个文件进行手动下载，耗时耗力。zqthu的项目解决了下载诸如 `https://cloud.tsinghua.edu.cn/f/2c50c14239b641d09632/`或者是 `https://cloud.tsinghua.edu.cn/d/36320b3f8a86487c931a/`中的所有文件的功能，非常好用。然而我们往往不需要下载整个共享文件夹，而只需要下载其中的一部分，比如 `https://cloud.tsinghua.edu.cn/d/dd37da8463504030aec9/?p=%2F07-14%20Git&mode=list`，本项目主要解决的就是这个问题。此外，除了别人共享给我们的文件夹，本项目还可以批量下载自己的清华云盘资料库中的文件，比如 `https://cloud.tsinghua.edu.cn/library/de8848df-a8a2-4775-9733-781c9b1aed73/PPT%E6%A8%A1%E6%9D%BF/。`本项目还添加了大量的描述信息，方便用户追踪当前的下载进度。

> 代码中和README中提到的清华云盘链接示例都是不存在的链接

# 介绍

This is a script to download files from Tsinghua Cloud.

Based on Github project of zqthu. link: https://github.com/zqthu/thu_cloud_download

可下载他人共享的清华云盘链接或者自己的资料库中的所有文件，只要输入需要下载的链接即可。

注意：如果是下载资料库中的文件，需要先登录清华云盘，然后将Cookie.txt中的内容替换为自己的Cookie。

查找自己的Cookie的方法可自行上网搜索。

# 用法

直接下载exe文件，双击打开，根据示例输入清华云盘的url即可。下载的文件位于当前目录下的 `Download`目录下。

也可以在py文件所在路径下打开cmd，输入python TsinghuaCloudDownload.py即可运行。

也欢迎其他同学基于py文件进行修改、补充。

另：运行脚本时不要开代理。


[tsinghua_cloud]: https://cloud.tsinghua.edu.cn
[mit_licence]: https://github.com/zqthu/thu_cloud_download/blob/master/LICENSE
