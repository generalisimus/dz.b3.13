class Tag:
	def __init__(self, tag, is_sing=None, klass=None, **kwargs):
		self.tag = tag
		self.is_sing = is_sing
		self.kids = []
		self.text = ""
		self.attribute = {}

		if klass is not None:
			self.attribute["class"] = " ".join(klass)

		for attr, value in kwargs.items():
			if "_" in attr:
				attr = attr.replace("_", "-")
			self.attribute[attr] = value


	def __enter__(self, **kwargs):
		return self

	def __exit__(self,*args):
		pass

	def __iadd__(self, other):
		self.kids.append(other)
		return self

	def __str__(self):
		attrs = []
		for attributes, value in self.attribute.items():
			attrs.append("%s = '%s'" % (attributes, value))
		attrs = " ".join(attrs)

		if len(self.kids):
		    opens = f'<{self.tag} {attrs}>'
		    if self.text:
		        inside = "%s" % self.text
		    else:
		    	inside = ""
		    for kid in self.kids:
		    	inside += str(kid)
		    end = "</%s" % self.tag
		    return opens + inside + end
		else:
			if self.is_sing:
				return f'<{self.tag} {attrs}/>'
			else:
				return f'<{self.tag} {attrs}>{self.text}</{self.tag}>'

class HTML:
    def __init__(self, output=None):
	    self.output = output
	    self.kids = []

    def __iadd__(self, other):
        self.kids.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self,*args):
    	if self.output is not None:
    		with open(self.output, "w") as fp:
    			fp.write(str(self))
    	else:
            print(self)

    def __str__(self):
    	html = "<html>\n"
    	for kid in self.kids:
    		html += str(kid)
    	html += "\n<html>"
    	return html

class TopLevelTag:
	def __init__(self, tag, **kwargs):
		self.tag = tag 
		self.kids = []

	def __iadd__(self, other):
		self.kids.append(other)
		return self

	def __enter__(self):
		return self

	def __exit__(self, *args):
		pass

	def __str__(self):
		html = "<%s>\n" % self.tag
		for kid in self.kids:
			html += str(kid)
		html += "\n</%s>" % self.tag
		return html


def main(output=None):

    with HTML(output=output) as doc:
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

                with Tag(
                    "img", is_single=True, src="/icon.png", data_image="responsive"
                ) as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main()
