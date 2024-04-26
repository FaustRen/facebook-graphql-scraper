# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class PageXpath(object):
    CLOSE_LOGIN_BUTTON = "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/i"


class PageClass(object):
    DISPLAY_MORE = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"
    CONTENTS = "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"
    CAPTION = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"
    CAPTION2 = "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"
    POSTDATE = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"
    POSTDATE = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"
    LIKES = "x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62"
    COMMENT_SHARE_PARENTS = "x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj"
    COMMENT_SHARE_CHILD = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"


class SoupElement(object):
    pass


class PageText(object):
    DISPLAY_MORE = "查看更多"
    DISPLAY_MORE2 = "顯示更多"


class PageRoleValue(object):
    DISPLAY_MORE = "button"


class PageLocators(object):
    CLOSELOGIN = (
        By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/i")
    DISPLAY_MORE = (
        By.XPATH, f"//div[@class='{PageClass.DISPLAY_MORE}' and @role='{PageRoleValue.DISPLAY_MORE}' and text()='{PageText.DISPLAY_MORE}']")

    LOGGINUSR1 = (
        "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input"
    )
    LOGGINPWD1 = (
        "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input"
    )
    
    LOGGINUSR2 = (
        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[2]/form/div/div[3]/div/label/div/div/input")
    LOGGINPWD2 = (
        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[2]/form/div/div[4]/div/label/div/div/input")

    # version.3: facebook login page
    LOGGINUSR3 = (By.NAME, "email")
    LOGGINPWD3 = (By.NAME, "pass")