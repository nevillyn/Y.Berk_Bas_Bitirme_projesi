from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import unittest


class TestInsiderCareers(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)


    def take_screenshot(self, name):
        self.driver.save_screenshot(f"{name}.png")

    def test_insider_careers(self):
        driver = self.driver

        # Visit https://useinsider.com/
        driver.get("https://useinsider.com/")
        time.sleep(1)
        # Cookies
        try:
            accept_cookies_button = driver.find_element(By.ID, "wt-cli-accept-all-btn")
            accept_cookies_button.click()
            print("Cookies accepted.")
        except Exception as e:
            print(f"Error accepting cookies: {e}")
            self.take_screenshot("cookies_error")
            return

        # Check if Insider homepage is opened
        try:
            assert "Insider" in driver.title
            print("Insider homepage is opened.")
        except AssertionError:
            print("Insider homepage is not opened.")
            self.take_screenshot("homepage_error")
            return

        # Select the "Company" menu in the navigation bar, select "Careers"
        try:
            company_menu = driver.find_element(By.XPATH, "/html/body/nav/div[2]/div/ul[1]/li[6]/a")
            company_menu.click()
            time.sleep(1)
            careers_menu = driver.find_element(By.XPATH, "/html/body/nav/div[2]/div/ul[1]/li[6]/div/div[2]/a[2]")
            careers_menu.click()
            time.sleep(1)
            print("Navigated to Careers page.")
        except Exception as e:
            print(f"Error navigating to Careers page: {e}")
            self.take_screenshot("careers_page_error")
            return
        time.sleep(2)

        # Check if the Locations, Teams, and Life at Insider blocks are open
        try:
            driver.find_element(By.ID, "career-our-location")
            driver.find_element(By.ID, "career-find-our-calling")
            driver.find_element(By.XPATH, "/html/body/div[2]/section[4]")
            print("Locations, Teams, and Life at Insider blocks are present.")
        except Exception as e:
            print(f"Error finding blocks: {e}")
            self.take_screenshot("blocks_error")
            return

        # Go to https://useinsider.com/careers/quality-assurance/, click "See all QA jobs"
        driver.get("https://useinsider.com/careers/quality-assurance/")
        time.sleep(3)
        try:
            see_all_qa_jobs = driver.find_element(By.XPATH,"/html/body/div[2]/section[1]/div/div/div/div["
                                                           "1]/div/section/div/div/div[1]/div/div/a")
            see_all_qa_jobs.click()
            # Time sleep 30 kullanmak yerine ilan sayısı yüklendiği zamanı beklemeyi tercih ettim.
            # Zamanımın çoğunu bu kısım aldı sayfa testi yürütürken aşırı yavaş yükleniyor.

            try:
                WebDriverWait(driver, 40).until(
                    EC.text_to_be_present_in_element((By.ID, "deneme"), "178")
                )
                print("Element contains the text '178'. Continuing with the test.")
            except TimeoutException:
                print("Timed out waiting for the text '178'. Test aborted.")
                self.take_screenshot("text_178_not_found")
                return

            print("Job list is loaded.")
        except Exception as e:
            print(f"Error clicking 'See all QA jobs': {e}")
            self.take_screenshot("see_all_qa_jobs_error")
            return

        # Filter jobs by Location: "Istanbul, Turkey", and Department: "Quality Assurance"
        try:
            location_filter = driver.find_element(By.ID, "select2-filter-by-location-container")
            time.sleep(1)
            location_filter.click()
            time.sleep(1)
            istanbul_option = driver.find_element(By.XPATH,
                                                  "/html/body/span/span/span[2]/ul/li[2]")
            istanbul_option.click()
            time.sleep(5)
            print("Jobs filtered by Location and Department.")
        except Exception as e:
            print(f"Error filtering jobs: {e}")
            self.take_screenshot("filter_jobs_error")
            return

        # Check the presence of the job list
        try:
            jobs_list = driver.find_elements(By.ID, "jobs-list")  # Adjust selector if necessary
            assert len(jobs_list) > 0
            print("Job list is present.")
        except AssertionError:
            print("No jobs found.")
            self.take_screenshot("job_list_error")
            return
        except Exception as e:
            print(f"Error finding job list: {e}")
            self.take_screenshot("job_list_error")
            return

        for job in jobs_list:
            try:
                position = job.find_element(By.XPATH, "/html/body/section[3]/div/div/div[2]/div[1]/div/p").text
                department = job.find_element(By.XPATH,
                                              "/html/body/section[3]/div/div/div[2]/div[1]/div/span").text
                location = job.find_element(By.XPATH, "/html/body/section[3]/div/div/div[2]/div[1]/div/div").text
                assert "Quality Assurance" in position
                assert "Quality Assurance" in department
                assert "Istanbul, Turkey" in location
                print(f"Job details are correct: {position}, {department}, {location}")
            except AssertionError:
                print(f"Job details are incorrect.")
                self.take_screenshot("job_details_error")
                return
            except Exception as e:
                print(f"Error checking job details: {e}")
                self.take_screenshot("job_details_error")
                return

        # Click the "View Role" button and check redirection
        try:

            hover_element = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div[2]/div[1]/div")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hover_element)
            time.sleep(2)

            actions = ActionChains(driver)
            actions.move_to_element(hover_element).perform()
            time.sleep(2)

            view_role_button = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div[2]/div[1]/div/a")
            view_role_button.click()
            time.sleep(5)
            browser_tabs = driver.window_handles
            driver.switch_to.window(browser_tabs[1])
            assert "jobs.lever.co/useinsider/" in driver.current_url
            print("Redirected to Lever Application form page.")
        except AssertionError:
            print("Redirection to Lever Application form page failed.")
            self.take_screenshot("view_role_error")
        except Exception as e:
            print(f"Error clicking 'View Role': {e}")
            self.take_screenshot("view_role_error")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
