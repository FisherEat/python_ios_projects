#coding:gbk
from filecmp import dircmp


def show_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left,dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        show_diff_files(sub_dcmp)

def show_only(dcmp):
    if dcmp.left_only:
        ave_rst = 1
        for i in dcmp.left_only:
            print("%s只存在于%s中"%(i,dcmp.left))
    if dcmp.right_only:
        for i in dcmp.right_only:
            print("%s只存在于%s中"%(i,dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        show_only(sub_dcmp)

def compare(dir1,dir2):
    dcmp = dircmp(dir1,dir2)
    show_diff_files(dcmp)
    show_only(dcmp)