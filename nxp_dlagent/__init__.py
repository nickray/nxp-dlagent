#!/usr/bin/env python
# coding: utf-8

"""Download agent for NXP material"""

__version__ = "0.1.0"

import getpass
import os
import pathlib
import shutil
import sys
import tempfile
import time

import selenium.common.exceptions as exceptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

HEADLESS = True

MIMETYPES = ";".join(
    [
        "application/octet-stream",
        "application/x-octet-stream",
        "application/pdf",
        "application/x-pdf",
        "application/zip",
    ]
)

# https://stackoverflow.com/a/287944
PROMPT_COLOUR_CODE = "\033[93m"
END_COLOUR_CODE = "\033[0m"


def colour_wrap(s):
    return PROMPT_COLOUR_CODE + s + END_COLOUR_CODE


# setup


def make_browser(dl_dir, headless=HEADLESS, mimetypes=MIMETYPES):

    options = Options()

    # these are some sticky settings that override the auto-download of PDFs
    options.set_preference("pdfjs.disabled", True)
    options.set_preference("pdfjs.enabledCache.state", False)

    # prevent the popup on what to do with the download and where to store it
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.focusWhenStarting", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.dir", dl_dir)
    options.set_preference("browser.download.manager.useWindow", False)

    options.set_preference("browser.helperApps.neverAsk.openFile", mimetypes)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", mimetypes)

    # toggle for visibility / debugging
    options.headless = headless

    # create the browser (driver)
    browser = Firefox(options=options, log_path="/dev/null")

    return browser


# def make_browser2(dl_dir, headless=HEADLESS, mimetypes=MIMETYPES):

#     global browser_tempdir
#     browser_tempdir = tempfile.TemporaryDirectory()
#     print(browser_tempdir.name)

#     profile = FirefoxProfile(browser_tempdir.name)

#     profile.set_preference("pdfjs.disabled", True)
#     profile.set_preference("pdfjs.enabledCache.state", False);

#     profile.set_preference("browser.download.folderList", 2)
#     profile.set_preference("browser.download.manager.focusWhenStarting", False);
#     profile.set_preference("browser.download.manager.showWhenStarting", False)
#     profile.set_preference("browser.download.manager.showAlertOnComplete", False);
#     profile.set_preference("browser.download.dir", dl_dir)
#     profile.set_preference("browser.download.manager.useWindow", False);

#     profile.set_preference("browser.helperApps.neverAsk.openFile", mimetypes);
#     profile.set_preference("browser.helperApps.alwaysAsk.force", False);
#     profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mimetypes)

#     options = Options()
#     options.headless = headless

#     profile.options = options

#     browser = Firefox(firefox_profile=profile)
#     return browser

# NB: this assumes the directory was empty before download started!
def download_complete(directory, verbose=False):
    directory = pathlib.Path(directory)
    glob = list(directory.glob("*"))
    if len(glob) == 0:
        if verbose:
            print("no files downloading yet")
        return False
    if len(glob) > 1:
        if verbose:
            print("files still downloading")
        return False

    path = glob[0]

    if path.name.endswith(".part"):
        if verbose:
            print("partial download")
        return False

    return glob[0]


def get_username():
    input(colour_wrap("Enter NXP account Email Address or NXP Company ID: "))


def get_password():
    getpass.getpass(colour_wrap("Enter NXP account password: "))


def get_username_password():
    if "NXP_USERNAME" in os.environ:
        username = os.environ["NXP_USERNAME"]
    else:
        username = get_username()

    if "NXP_PASSWORD" in os.environ:
        password = os.environ["NXP_PASSWORD"]
    else:
        password = get_password()

    return username, password


def main():
    with tempfile.TemporaryDirectory() as dl_directory:

        # get it
        if len(sys.argv) != 2:
            print("Pass specific colCode to download!")
            sys.exit(1)

        col_code = sys.argv[1]
        if col_code.startswith("nxp://"):
            col_code = col_code[len("nxp://") :]
        url = f"https://www.nxp.com/webapp/Download?colCode={col_code}&appType=license"
        print(f"url: {url}")

        # print(sys.argv)
        username, password = get_username_password()

        print(f"download dir: {dl_directory}")
        browser = make_browser(dl_directory)
        # browser = make_browser2(dl_directory)

        # load page
        browser.get(url)

        # login with username/password
        browser.find_element_by_id("username").send_keys(username)
        browser.find_element_by_id("password").send_keys(password)
        browser.find_element_by_name("loginbutton").click()

        # wait for license acceptance page to appear
        while True:
            if download_complete(dl_directory):
                break
            try:
                browser.find_element_by_name("Submit").click()
                break
            except exceptions.NoSuchElementException:
                time.sleep(1)

        # download file
        print("waiting for download")
        while not download_complete(dl_directory):
            time.sleep(1)

        browser.quit()

        # move file to working directory
        filepath = download_complete(dl_directory)
        print(f"here it is: {filepath}")
        filename = pathlib.Path(".") / filepath.name
        shutil.move(filepath, filename)

        print(f"Downloaded {filename}")


if "__main__" == __name__:
    main()
