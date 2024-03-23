import os

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


"""
向一个树组件中逐层检查是否存在待添加节点，如果不存在则添加。常见的场景是url和文件结构
treeWidget: 待操作的树组件对象
pathArr: 待添加字符串按节点分割
index: 对应节点序号
parent: 对应节点序号的父节点
"""


def treeWidget_addPathArr(treeWidget: QTreeWidget, pathArr: list, index: int = 0, parent: QTreeWidgetItem = None):
    item = None
    # 顶级节点查询
    if index == 0:
        for j in range(treeWidget.topLevelItemCount()):
            if pathArr[0] == treeWidget.topLevelItem(j).text(0):
                item = treeWidget.topLevelItem(j)
                break
        parent = treeWidget
    # 非顶级节点查询
    else:
        for j in range(parent.childCount()):
            if pathArr[index] == parent.child(j).text(0):
                item = parent.child(j)
                break
    # 不存在,则在父节点下创建
    if item is None:
        item = QTreeWidgetItem(parent)
        item.setText(0, pathArr[index])
    # 判断是否存在次一级的节点
    index = index + 1
    if index < len(pathArr):
        treeWidget_addPathArr(treeWidget=treeWidget, pathArr=pathArr, index=index, parent=item)


"""
读取指定目录下的py文件，加载到树组件中
@file_search 文件名搜索
"""


def load_script(dir_path: str, treeWidget: QTreeWidget, file_search=''):
    treeWidget.clear()
    name_list = os.listdir(dir_path)
    for i in range(len(name_list)):
        load_script_sub(name=name_list[i], parent_dirPath=dir_path, treeWidget=treeWidget, file_search=file_search)


def load_script_sub(name: str, parent_dirPath: str, treeWidget: QTreeWidget, parent: QTreeWidgetItem = None,
                    file_search=''):
    if os.path.isdir(parent_dirPath + '/' + name):
        item = QTreeWidgetItem([name])
        if parent is None:
            treeWidget.addTopLevelItem(item)
        else:
            parent.addChild(item)
        name_list = os.listdir(parent_dirPath + '/' + name)
        for i in range(len(name_list)):
            load_script_sub(name=name_list[i], parent_dirPath=parent_dirPath + '/' + name, treeWidget=treeWidget,
                            parent=item)
    elif name.endswith('.py'):
        # 空字符串可以在任何字符串中
        if file_search.lower() not in name.lower():
            return
        item = QTreeWidgetItem([name])
        if parent is None:
            treeWidget.addTopLevelItem(item)
        else:
            parent.addChild(item)


"""
获取树组件中点击节点对应的路径
"""


def treeWidget_getPath(item: QTreeWidgetItem, separator='/'):
    # 获取点击节点路径
    item_path = item.text(0)
    while True:
        item = item.parent()
        if item is not None:
            item_path = item.text(0) + '/' + item_path
        else:
            break
    return item_path
