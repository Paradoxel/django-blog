from django.test import TestCase
from django.urls import reverse


class CoreViewTest(TestCase):
    # set up
    def setUp(self):
        self.home_url = reverse('core:home')
        self.contact_url=reverse('core:contact')
        self.about_url=reverse('core:about')

    # Home
    def test_home_page_status_code(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_home_page_contains_expected_text(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, "Travel")

    def test_home_page_contains_contact_link(self):
        response = self.client.get(self.home_url)
        self.assertContains(response, self.contact_url)


    # Contact 
    def test_contact_page_status_code(self):
        response=self.client.get(self.contact_url)
        self.assertEqual(response.status_code,200)

    def test_contact_page_uses_correct_template(self):
        response=self.client.get(self.contact_url)
        self.assertTemplateUsed(response,'core/contact.html')

    def test_contact_page_contains_expected_text(self):
        response=self.client.get(self.contact_url)
        self.assertContains(response,"Contact Us")


    # contact
    def test_about_page_status_code(self):
        response =self.client.get(self.about_url)
        self.assertEqual(response.status_code,200)

    def test_about_page_uses_correct_template(self):
        response=self.client.get(self.about_url)
        self.assertTemplateUsed(response,'core/about.html')

    def test_about_page_contains_expected_text(self):
        response=self.client.get(self.about_url)
        self.assertContains(response,"About Us")

