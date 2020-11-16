from pathlib import Path
from importlib import import_module
import pydoc
import os


def import_all_files(folder: Path, i_list):
    for sub_file in folder.iterdir():
        if sub_file.is_file() and sub_file.suffix == ".py":
            i_list.append(import_module(str(sub_file).replace("\\", ".")[:-3]))
        if sub_file.is_dir():
            import_all_files(sub_file, i_list)


def write_index(modules: list):
    start = """<!DOCTYPE html>
<html><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta charset="UTF-8">
<style type="text/css">
:root {
  font-family: sans-serif;
}
img {
  border: 0;
}
th {
  text-align: start;
  white-space: nowrap;
}
th > a {
  color: inherit;
}
table[order] > thead > tr > th {
  cursor: pointer;
}
table[order] > thead > tr > th::after {
  display: none;
  width: .8em;
  margin-inline-end: -.8em;
  text-align: end;
}
table[order="asc"] > thead > tr > th::after {
  content: "\2193"; /* DOWNWARDS ARROW (U+2193) */
}
table[order="desc"] > thead > tr > th::after {
  content: "\2191"; /* UPWARDS ARROW (U+2191) */
}
table[order][order-by="0"] > thead > tr > th:first-child > a ,
table[order][order-by="1"] > thead > tr > th:first-child + th > a ,
table[order][order-by="2"] > thead > tr > th:first-child + th + th > a {
  text-decoration: underline;
}
table[order][order-by="0"] > thead > tr > th:first-child::after ,
table[order][order-by="1"] > thead > tr > th:first-child + th::after ,
table[order][order-by="2"] > thead > tr > th:first-child + th + th::after {
  display: inline-block;
}
table.remove-hidden > tbody > tr.hidden-object {
  display: none;
}
td {
  white-space: nowrap;
}
table.ellipsis {
  width: 100%;
  table-layout: fixed;
  border-spacing: 0;
}
table.ellipsis > tbody > tr > td {
  padding: 0;
  overflow: hidden;
  text-overflow: ellipsis;
}
/* name */
/* name */
th:first-child {
  padding-inline-end: 2em;
}
/* size */
th:first-child + th {
  padding-inline-end: 1em;
}
td:first-child + td {
  text-align: end;
  padding-inline-end: 1em;
}
/* date */
td:first-child + td + td {
  padding-inline-start: 1em;
  padding-inline-end: .5em;
}
/* time */
td:first-child + td + td + td {
  padding-inline-start: .5em;
}
.symlink {
  font-style: italic;
}
.dir ,
.symlink ,
.file {
  margin-inline-start: 20px;
}
.dir::before ,
.file > img {
  margin-inline-end: 4px;
  margin-inline-start: -20px;
  max-width: 16px;
  max-height: 16px;
  vertical-align: middle;
}
.dir::before {
  content: url(resource://content-accessible/html/folder.png);
}
</style>
<link rel="stylesheet" media="screen, projection" type="text/css" href="chrome://global/skin/dirListing/dirListing.css">
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8%2F9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAjFJREFUeNqsU8uOElEQPffR3XQ3ONASdBJCSBxHos5%2B3Bg3rvkCv8PElS78gPkO%2FATjQoUdO2ftrJiRh6aneTb9sOpC4weMN6lcuFV16pxDIfI8x12OYIDhcPiu2Wx%2B%2FHF5CW1Z6Jyegt%2FTNEWSJIjjGFEUIQxDrFYrWFSzXC4%2FdLvd95pRKpXKy%2BpRFZ7nwaWo1%2BsGnQG2260BKJfLKJVKGI1GEEJw7ateryd0v993W63WEwjgxfn5obGYzgCbzcaEbdsIggDj8Riu6z6iUk9SYZMSx8W0LMsM%2FSKK75xnJlIq80anQXdbEp0OhcPJ0eiaJnGRMEyyPDsAKKUM9clkYoDo3SZJzzSdp0VSKYmfV1co%2Bz580kw5KDIM8RbRfEnUf1HzxtQyMAGcaGruTKczMzEIaqhKifV6jd%2BzGQQB5llunF%2FM52BizC2K5sYPYvZcu653tjOM9O93wnYc08gmkgg4VAxixfqFUJT36AYBZGd6PJkFCZnnlBxMp38gqIgLpZB0y4Nph18lyWh5FFbrOSxbl3V4G%2BVB7T4ajYYxTyuLtO%2BCvWGgJE1Mc7JNsJEhvgw%2FQV4fo%2F24nbEsX2u1d5sVyn8sJO0ZAQiIYnFh%2BxrfLz%2Fj29cBS%2FO14zg3i8XigW3ZkErDtmKoeM%2BAJGRMnXeEPGKf0nCD1ydvkDzU9Jbc6OpR7WIw6L8lQ%2B4pQ1%2FlPF0RGM9Ns91Wmptk0GfB4EJkt77vXYj%2F8m%2B8y%2FkrwABHbz2H9V68DQAAAABJRU5ErkJggg%3D%3D">
<title>Documentation Reference</title>
<!-- base href="file:///C:/Users/Fedacking/source/piton/Microscopy-Program/Documentation/ReferenceDatabase/" -->
</head>
<body dir="ltr">
<h1>Documentation Reference</h1>
<table order="">
 <thead>
  <tr>
   <th><a href="">Name</a></th>
  </tr>
 </thead>
 <tbody>"""
    end = """"</tbody></table>
</body></html>"""
    for module in modules:
        name = getattr(module, '__name__', None)
        start += """<tr> <td sortable-data=\"""" + name + """.html"><table class="ellipsis"><tbody><tr><td><a class="file" href="ReferenceDatabase/""" + name + """.html"><img src="ReferenceDatabase/a" alt="File:">""" + name + """.html</a></td></tr></tbody></table></td> </tr> """
    start += end
    index_file = open("Documentation Reference.html", "w+")
    index_file.write(start)
    index_file.close()


main_folder = Path(".")
import_list = []
for file in main_folder.iterdir():
    if file.is_dir():
        import_all_files(file, import_list)
os.chdir("Documentation\\ReferenceDatabase")
for imported_file in import_list:
    pydoc.writedoc(imported_file)
os.chdir("..")
write_index(import_list)