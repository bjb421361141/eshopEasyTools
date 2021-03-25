# coding=utf-8
import xlwt


class ExcelUtil(object):
    """
        03版excel 文件保存
    """
    # 锁定类的变量，实例对象或类无法再添加属性
    __slots__ = ("__row0", "__savePath", "__workbook")

    def __init__(self, row0, savepath):
        self.__row0 = row0
        self.__savePath = savepath
        self.__workbook = xlwt.Workbook()  # 默认生成一个 workbook 对象

    def get_save_path(self):
        return self.__savePath

    def set_save_path(self, value):
        self.__savePath = value

    def print_save_path(self):
        print('文件保存路径: %s' % self.__savePath)

    # 创建表头信息
    def __creat_header(self, sheet):
        for i in range(0, len(self.__row0)):
            sheet.write(0, i, self.__row0[i], self.set_stlye("Time New Roman", 220, True))
        return

    # 设置表格样式
    def set_stlye(self, name="Arial", height=200, bold=False):
        # 初始化样式
        style = xlwt.XFStyle()
        # 创建字体
        font = xlwt.Font()
        font.bold = bold
        font.colour_index = 4
        font.height = height
        # font.name = name
        style.font = font
        return style

    def write_excel(self, sheetName, sheetData):
        # 获取 sheet 页
        sheet = None
        if sheetName is not None:
            sheet = self.__workbook.add_sheet(sheetName, cell_overwrite_ok=True)
            # sheet = self.__workbook.get_sheet(sheetName)
            # if sheet is None:
            #     sheet = self.__workbook.add_sheet(sheetName, cell_overwrite_ok=True)
        else:
            sheet = self.__workbook.add_sheet(u'sheet1', cell_overwrite_ok=True)

        # 创建表头
        if self.__row0 is not None:
            self.__creat_header(sheet)

        # 填充数据
        for i in range(0, len(sheetData)):
            for j in range(0, len(self.__row0)):
                sheet.write(i+1, j, sheetData[i][j], self.set_stlye('Times New Roman'))

    def save(self):
        self.__workbook.save(self.__savePath)
