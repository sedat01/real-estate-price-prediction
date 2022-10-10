import link_scrapers
import property_explorer_requests


sitemap_url="https://www.immoweb.be/sitemap.xml"
property_type="house"

#link_scrapers.xml_scrape(sitemap_url,property_type)
property_explorer_requests.explorer(10)