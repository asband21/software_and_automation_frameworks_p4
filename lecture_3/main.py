import xml.sax


class matrix:
    def __init__(self,high,width,var = 0):
        self.high = high
        self.width = width
        self.array = [[var for x in range(width)] for y in range(high)]

    def __repr__(self):
        string = ""
        for x in range(self.high):
            for y in range(self.width):
                string = string + str(self.array[y][x]) + "  "
                #print(self.array[x])
            string = string+"\n"

        return string

    def write_value(self, x, y, value):
        self.array[y][x] = value

    def multiply(self,var):
        for x in range(self.width):
            for y in range(self.high):
                self.array[y][x] = self.array[y][x] * var

    def transpose(self):
        mid_array = [[0 for x in range(self.high)] for y in range(self.width)]
        for x in range(self.width):
            for y in range(self.high):
                mid_array[x][y] = self.array[y][x]
        self.array = mid_array

    def print_to_XML(self):
        string_XML ="<matrix>\n\t<high>" + str(self.high) + "</high>\n\t<width>" + str(self.width) + "</width>\n\t<values>"
        for x in range(self.width):
            for y in range(self.high):
                string_XML = string_XML + "\n\t\t<number>" + str(self.array[y][x]) + "</number>"
        string_XML= string_XML + "\n\t</values>" + "\n</matrix>"
        return string_XML

class MyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_element = ""
    def startElement(self, name, attrs):
        self.current_element = name
       # print("Start element:", name)
        for attr in attrs.getNames():
           # print("Attribute:", attr, "=", attrs.getValue(attr))
            pass
    def endElement(self, name):
        pass
        #print("End element:", name)
    def characters(self, content):
        if self.current_element == "high" and content is not None:
            print("High: SHahab", not content)
        elif self.current_element == "width":
            pass
           # print("Width:", content)
        elif self.current_element == "number":
            pass
            #print("Number:", content)

handler = MyHandler()
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
parser.parse("matrix_XML.xml")

R = matrix(3, 3, var=2)
#print(R.array)
R.transpose()
#print(".......")
#print(R.array)
print(R)
print(R.print_to_XML())



