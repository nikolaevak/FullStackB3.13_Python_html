# B3.13 Домашнее задание
import html
class HTML:
    def __init__(self, output="test.html"):
        self.tags_list =[]
        self.output = output

    def __iadd__(self, other):
        self.tags_list.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as file:
                file.write(str(self))
        else:
            print(self)


    def __str__(self):
        toplevel = "<html>\n"
        for onetag in self.tags_list:
            toplevel +=str(onetag)
        toplevel +="\n</html>"
        return toplevel

class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.tags_list = []

    def __iadd__(self, other):
        self.tags_list.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        toplevel = "<%s>\n"%self.tag
        for onetag in self.tags_list:
            toplevel +=str(onetag)
        toplevel += "\n</%s>"%self.tag
        return toplevel


class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.text = ""
        self.attributes = {}
        self.tags_list = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr.replace("_","-")
            self.attributes[attr] = value

    def __iadd__(self, other):
        self.tags_list.append(other)
        return self


    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        tags_list = []
        for attribute, value in self.attributes.items():
            tags_list.append('%s="%s"' % (attribute,value))
        tags_list = " ".join(tags_list)
        # return tags_list

        if self.tags_list:
            start = "<{tag} {attr}>".format(tag=self.tag, attr=tags_list)
            internal = "%s" % self.text
            for onetag in self.tags_list:
                internal += str(onetag)
            end = "</%s>" % self.tag
            return start + internal + end

        else:
            if self.is_single:
                return "<{tag} {attr}/>".format(tag=self.tag, attr= tags_list)
            else:
                return "<{tag} {attr}>{text}</{tag}>".format(tag = self.tag, attr=tags_list, text=self.text)

# <html>
# <head>
#   <title>hello</title>
# </head>
# <body>
#     <h1 class="main-text">Test</h1>
#     <div class="container container-fluid" id="lead">
#         <p>another test</p>
#         <img src="/icon.png" data-image="responsive"/>
#     </div>
# </body>
# </html>
with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body