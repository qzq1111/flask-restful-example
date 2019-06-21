import os

import xlsxwriter
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from flask import current_app
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Image, PageBreak, Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


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


def word_write(generated_doc_path):
    # 模板路径文件夹
    template_path = current_app.config.get("REPORT_TEMPLATES")
    path = os.path.join(template_path, 'test.docx')

    # 读取指定位置的模板文件
    doc = DocxTemplate(path)
    # 渲染的内容
    context = {
        # 标题
        'title': "人员信息",
        # 表格
        'table': [
            {"name": "小李", "age": 11},
            {"name": "小张", "age": 21},
            {"name": "小张", "age": 20},
            {"name": "小张1", "age": 10},
            {"name": "小张2", "age": 30},
            {"name": "小张3", "age": 40},
        ],
        # 页眉
        'header': 'xxx公司人员信息管理',
        # 页脚
        'footer': '1',
        # 图片
        'image': InlineImage(doc, os.path.join(template_path, 'test.jpg'), height=Mm(10)),
    }
    # 渲染模板
    doc.render(context)

    # 保存渲染的文件
    doc.save(generated_doc_path)
    return generated_doc_path


def table_model():
    """
    添加表格
    :return:
    """
    template_path = current_app.config.get("REPORT_TEMPLATES")
    image_path = os.path.join(template_path, 'test.jpg')
    new_img = Image(image_path, width=300, height=300)
    base = [
        [new_img, ""],
        ["大类", "小类"],
        ["WebFramework", "django"],
        ["", "flask"],
        ["", "web.py"],
        ["", "tornado"],
        ["Office", "xlsxwriter"],
        ["", "openpyxl"],
        ["", "xlrd"],
        ["", "xlwt"],
        ["", "python-docx"],
        ["", "docxtpl"],
    ]

    style = [
        # 设置字体
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),

        # 合并单元格 (列,行)
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 2), (0, 5)),
        ('SPAN', (0, 6), (0, 11)),

        # 单元格背景
        ('BACKGROUND', (0, 1), (1, 1), HexColor('#548DD4')),

        # 字体颜色
        ('TEXTCOLOR', (0, 1), (1, 1), colors.white),
        # 对齐设置
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        # 单元格框线
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),

    ]

    component_table = Table(base, style=style)
    return component_table


def paragraph_model(msg):
    """
    添加一段文字
    :param msg:
    :return:
    """
    # 设置文字样式
    style = ParagraphStyle(
        name='Normal',
        fontName='SimSun',
        fontSize=50,
    )

    return Paragraph(msg, style=style)


def image_model():
    """
    添加图片
    :return:
    """
    template_path = current_app.config.get("REPORT_TEMPLATES")
    image_path = os.path.join(template_path, 'test.jpg')
    new_img = Image(image_path, width=300, height=300)
    return new_img


def pdf_write(generated_pdf_path):
    """
    生成pdf
    :return:
    """
    # 增加的字体，支持中文显示,需要自行下载支持中文的字体
    font_path = current_app.config.get("SIM_SUN")

    pdfmetrics.registerFont(TTFont('SimSun', os.path.join(font_path, 'SimSun.ttf')))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(fontName='SimSun', name='SimSun', leading=20, fontSize=12))
    data = list()
    # 添加一段文字
    paragraph = paragraph_model("测试添加一段文字")
    data.append(paragraph)
    data.append(PageBreak())  # 分页标识
    # 添加table和图片
    table = table_model()
    data.append(table)
    data.append(PageBreak())  # 分页标识
    img = image_model()
    data.append(img)

    # 设置生成pdf的名字和编剧
    pdf = SimpleDocTemplate(generated_pdf_path, rightMargin=0, leftMargin=0, topMargin=40, bottomMargin=0, )
    # 设置pdf每页的大小
    pdf.pagesize = (9 * inch, 10 * inch)

    pdf.multiBuild(data)
    return generated_pdf_path
