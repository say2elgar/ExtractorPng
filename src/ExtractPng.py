#!/opt/local/bin/python2.7
import sys
import Image
from xml.dom.minidom import parse, parseString

def extract_from_xml(xml_filename, png_filename):
	print 'XML File :', str(xml_filename), 'PNG File :', str(png_filename)
	# XML Parsing
	dom = parse(xml_filename)
	textures = dom.getElementsByTagName("SubTexture")
	big_image = Image.open(png_filename)

	for texture in textures:
		texture_name = texture.attributes.getNamedItem("name").nodeValue
		texture_name = texture_name.replace('parts/','')
		print 'Texture :', texture_name

		width = int(texture.attributes.getNamedItem("width").nodeValue)
		height = int(texture.attributes.getNamedItem("height").nodeValue)
		box = (
			int(texture.attributes.getNamedItem("x").nodeValue),
			int(texture.attributes.getNamedItem("y").nodeValue),
			int(texture.attributes.getNamedItem("x").nodeValue) + width,
			int(texture.attributes.getNamedItem("y").nodeValue) + height
			)
		rect_on_big = big_image.crop(box)
		extract_image = Image.new('RGBA', (width,height), (0,0,0,0))
		result_box = ( width,height )
		extract_image.paste(rect_on_big, (0,0), mask=0)
		outfile = texture_name+'.png'
		print outfile, "generated"
		extract_image.save(outfile)


if __name__ == '__main__' :
	try:
		filename = sys.argv[1]
	except Exception, err:
		sys.stderr.write('Usage : %s <filename>\n' % str(sys.argv[0]))
	else:
		extract_from_xml(filename+'.xml', filename+'.png')

