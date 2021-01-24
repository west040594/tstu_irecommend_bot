from bs4 import BeautifulSoup
from seleniumrequests import Firefox

from constants import IRECOMMEND_DOMAIN_NAME
from models import Review, Product


class RequestService:
    web_driver = Firefox()

    def get_product_info(self, product_request) -> Product:
        dom_model = self.form_soup_dom_model(product_request.url)
        product_rating = dom_model.find('span', {"class": "rating"})
        image_link = dom_model.find('div', {"class": "mainpic"}).find("img")["src"]
        product = Product()
        product.rating = product_rating.text
        product.image_url = image_link
        product.link_url = product_request.url
        product.name = product_request.product_name
        link_list = self.create_review_link_list(dom_model.find('ul', {"class": "list-comments"}))
        print(link_list)

        page_count = 1
        is_not_final_page = True

        while is_not_final_page:
            first_link_on_current_page = link_list[0]
            review_set = self.form_review_set(review_link_list=link_list)
            product.reviews.extend(review_set)
            dom_model = self.form_soup_dom_model(product_request.url + "?page=" + str(page_count))
            link_list = self.create_review_link_list(dom_model.find('ul', {"class": "list-comments"}))
            first_link_on_next_page = link_list[0]
            page_count += 1
            is_not_final_page = first_link_on_current_page != first_link_on_next_page

        return product

    def form_soup_dom_model(self, url) -> BeautifulSoup:
        response = self.web_driver.request('GET', url)
        return BeautifulSoup(response.text, 'html.parser')

    def form_review_set(self, review_link_list) -> set:
        reviews = set()
        for review_link in review_link_list:
            dom_model = self.form_soup_dom_model(review_link)
            review = Review()
            review.rating = dom_model.find('meta', {"itemprop": "ratingValue"})["content"]
            review.body = dom_model.find('div', {"itemprop": "reviewBody"}).text
            review.title = dom_model.find('h2', {"class": "reviewTitle"}).find("a").text
            review.read_link = review_link
            review.post_time = dom_model.find('span', {"class": "dtreviewed"}).text
            review.reviewer_name = dom_model.find("strong", {"class": "reviewer"}).find("a").text
            print("Получен отзыв: " + repr(review))
            reviews.add(review)
        return reviews

    # Создать список с урлами на отзывы
    def create_review_link_list(self, ulElement) -> []:
        review_link_list = []
        for sub in ulElement.find_all('li', recursive=False):
            review_link = sub.find('div', {"class": "reviewTitle"}).find("a")["href"]
            review_link_list.append(IRECOMMEND_DOMAIN_NAME + review_link)
        return review_link_list
