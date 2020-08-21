from lxml import etree

doc=etree.parse('E:\\Dropbox\\Projects and Freelance\\Bain\\AAGProducts\\python\\my_flask\\virtual\\LEGO Dashboard WIP.twb')
doc2='results.twb'

def remove(doc,path,note='Removed'):
    doc=doc
    i=0
    for elem in doc.xpath(path):
        parent = elem.getparent()
        comment = etree.Comment(note)
        while i < 10:
            parent.insert(1, comment)
            i=i+1
            print(i)
        parent.remove(elem)

remove(doc,"//*/color-palette")
remove(doc,"//*/thumbnails")
remove(doc,"//*/metadata-record")
remove(doc,"//*/style-rule/encoding[@attr='color']")
remove(doc,"//*/datasources/datasource/column[not(calculation)]")
remove(doc,"//*/column/calculation/members/member[attribute::value]")
remove(doc,"//*/datasource[@hasconnection='false'][@name='Parameters']")
remove(doc,"//*/dashboard/datasource-dependencies/column")
remove(doc,"//*/worksheet/table/view/datasource-dependencies/column[not(calculation)]")
#remove(doc,"//*/worksheet/table/view/datasource-dependencies/column-instance[not(table-calc) and not(calculation)]")

doc.write(doc2,pretty_print=True, xml_declaration=True,encoding="utf-8")