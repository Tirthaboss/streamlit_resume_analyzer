import xml.etree.ElementTree as ET
from datetime import datetime

def create_sitemap(urls):
    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in urls:
        doc = ET.SubElement(root, "url")
        loc = ET.SubElement(doc, "loc")
        loc.text = url
        lastmod = ET.SubElement(doc, "lastmod")
        lastmod.text = datetime.now().strftime("%Y-%m-%d")
        changefreq = ET.SubElement(doc, "changefreq")
        changefreq.text = "monthly"
        priority = ET.SubElement(doc, "priority")
        priority.text = "0.5"

    tree = ET.ElementTree(root)
    tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)

def main():
    urls = [
        "https://ai-resume-checker.streamlit.app/",
        # Add more URLs here
    ]

    create_sitemap(urls)
    print("Sitemap created successfully.")

if __name__ == "__main__":
    main()
