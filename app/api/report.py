import xlsxwriter


def excel_write(path):
    # 新建excel文本
    workbook = xlsxwriter.Workbook(path)
    # 添加一个sheet
    worksheet = workbook.add_worksheet("test1")
    # 设置列宽
    worksheet.set_column('A:A', 20)

    # 添加字体加粗样式
    bold = workbook.add_format({'bold': True})

    # 写入数据
    worksheet.write('A1', 'Hello')

    # 写入数据并使用样子
    worksheet.write('A2', 'World', bold)

    # 使用数字标识单元格位置（行，列）
    worksheet.write(2, 0, 123)
    worksheet.write(3, 0, 123.456)

    # 按行依次写入数据
    worksheet.write_column(4, 0, [1, 2, 3, 4])

    # 按列依次写入数据
    worksheet.write_row(1, 1, [1, 2, 3, 4])

    # 添加图表
    chart = workbook.add_chart({'type': 'column'})

    # 图表数据来源
    chart.add_series({'values': ["test1",  # worksheet的名字。即sheet_name
                                 4, 0, 7, 0  # 数据位置
                                 ]})
    # 插入的表格位置
    worksheet.insert_chart('B3', chart)

    # 关闭excel文本并输出到指定位置。如果不调用改方法，无法输出excel
    workbook.close()
    return path
