import time

import base64
import random
import re
import string
import zbarlight
from PIL import Image
from appium.webdriver.common.touch_action import TouchAction
from datetime import datetime
from eth_keys import datatypes
from io import BytesIO
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from support.device_apps import start_web_browser
from tests import common_password, pytest_config_global, geth_log_emulator_path, transl
from views.base_element import BaseButton, BaseElement, BaseEditBox, BaseText


# class BackButton(BaseButton):
#     def __init__(self, driver):
#         super(BackButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('back-button')
#
#     def click(self, times_to_click: int = 1):
#         for _ in range(times_to_click):
#             self.find_element().click()
#             self.driver.info('Tap on %s' % self.name)
#         return self.navigate()
#
#
# class AllowButton(BaseButton):
#     def __init__(self, driver):
#         super(AllowButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='Allow' or @text='ALLOW']")
#
#     def click(self, times_to_click=3):
#         try:
#             for _ in range(times_to_click):
#                 self.find_element().click()
#                 self.driver.info('Tap on %s' % self.name)
#         except NoSuchElementException:
#             pass
#
#
# class SearchEditBox(BaseEditBox):
#     def __init__(self, driver):
#         super(SearchEditBox, self).__init__(driver)
#         self.locator = self.Locator.text_selector("Search or type web address")
#
#
# class DenyButton(BaseButton):
#     def __init__(self, driver):
#         super(DenyButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='Deny' or @text='DENY']")
#
# class CancelButton(BaseButton):
#     def __init__(self, driver):
#         super(CancelButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='Cancel' or @text='CANCEL']")
#
# class DeleteButton(BaseButton):
#     def __init__(self, driver):
#         super(DeleteButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='DELETE']")
#
#
# class YesButton(BaseButton):
#     def __init__(self, driver):
#         super(YesButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='YES' or @text='GOT IT']")
#
#
# class NoButton(BaseButton):
#     def __init__(self, driver):
#         super(NoButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='No']")
#
#
# class OkButton(BaseButton):
#     def __init__(self, driver):
#         super(OkButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='OK'or @text='Ok']")
#
#
# class ContinueButton(BaseButton):
#     def __init__(self, driver):
#         super(ContinueButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='CONTINUE' or @text='Continue']")
#
#
# class TabButton(BaseButton):
#
#     @property
#     def counter(self):
#         class Counter(BaseText):
#             def __init__(self, driver, parent_locator):
#                 super(Counter, self).__init__(driver)
#                 self.locator = self.Locator.xpath_selector(
#                     "//*[@content-desc='%s']//android.view.ViewGroup[2]/android.widget.TextView" % parent_locator)
#
#         return Counter(self.driver, self.locator.value)
#
#     @property
#     def public_unread_messages(self):
#         class PublicChatUnreadMessages(BaseElement):
#             def __init__(self, driver):
#                 super(PublicChatUnreadMessages, self).__init__(driver)
#                 self.locator = self.Locator.accessibility_id('public-unread-badge')
#
#         return PublicChatUnreadMessages(self.driver)
#
#
# class HomeButton(TabButton):
#     def __init__(self, driver):
#         super(HomeButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('home-tab-button')
#
#     def navigate(self):
#         from views.home_view import HomeView
#         return HomeView(self.driver)
#
#     def click(self, desired_view='home'):
#         from views.home_view import PlusButton
#         from views.chat_view import ChatMessageInput, ProfileNicknameOtherUser
#         if desired_view == 'home':
#             element = PlusButton(self.driver)
#         elif desired_view == 'chat':
#             element = ChatMessageInput(self.driver)
#         elif desired_view == 'other_user_profile':
#             element = ProfileNicknameOtherUser(self.driver)
#         self.click_until_presence_of_element(element)
#         return self.navigate()
#
#
# class ShareButton(BaseButton):
#     def __init__(self, driver):
#         super(ShareButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('share-my-contact-code-button')
#
#
# class DappTabButton(TabButton):
#     def __init__(self, driver):
#         super(DappTabButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('dapp-tab-button')
#
#     def navigate(self):
#         from views.dapps_view import DappsView
#         return DappsView(self.driver)
#
#     def click(self, desired_element_text = 'enter_url'):
#         from views.dapps_view import EnterUrlEditbox
#         if desired_element_text == 'enter_url':
#             self.click_until_presence_of_element(EnterUrlEditbox(self.driver))
#         else:
#             base_view = BaseView(self.driver)
#             self.click_until_presence_of_element(base_view.element_by_text_part(desired_element_text))
#
#         return self.navigate()
#
#
# class WalletButton(TabButton):
#     def __init__(self, driver):
#         super(WalletButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('wallet-tab-button')
#
#     def navigate(self):
#         from views.wallet_view import WalletView
#         return WalletView(self.driver)
#
#     def click(self):
#         self.driver.info('Tap on %s' % self.name)
#         from views.wallet_view import MultiaccountMoreOptions
#         self.click_until_presence_of_element(MultiaccountMoreOptions(self.driver))
#         return self.navigate()
#
#
# class ProfileButton(TabButton):
#     def __init__(self, driver):
#         super(ProfileButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('profile-tab-button')
#
#     def navigate(self):
#         from views.profile_view import ProfileView
#         return ProfileView(self.driver)
#
#     def click(self, desired_element_text = 'privacy'):
#         from views.profile_view import PrivacyAndSecurityButton
#         if desired_element_text == 'privacy':
#             self.click_until_presence_of_element(PrivacyAndSecurityButton(self.driver))
#         else:
#             base_view = BaseView(self.driver)
#             self.click_until_presence_of_element(base_view.element_by_text_part(desired_element_text))
#         return self.navigate()
#
# class StatusButton(TabButton):
#     def __init__(self, driver):
#         super(StatusButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('status-tab-button')
#
#     def navigate(self):
#         from views.chat_view import ChatView
#         return ChatView(self.driver)
#
#     def click(self):
#         self.driver.info('Tap on %s' % self.name)
#         from views.chat_view import AddNewStatusButton
#         self.click_until_presence_of_element(AddNewStatusButton(self.driver))
#         return self.navigate()
#
# class SaveButton(BaseButton):
#     def __init__(self, driver):
#         super(SaveButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector(
#             "//android.widget.TextView[@text='Save']")
#
#
# class NextButton(BaseButton):
#     def __init__(self, driver):
#         super(NextButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector(
#             "//android.widget.TextView[@text='Next']")
#
#
# class AddButton(BaseButton):
#     def __init__(self, driver):
#         super(AddButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector(
#             "//android.widget.TextView[@text='Add']")
#
#
# class DoneButton(BaseButton):
#     def __init__(self, driver):
#         super(DoneButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@content-desc='done-button' or contains(@text, 'Done')]")
#
#
# class AppsButton(BaseButton):
#     def __init__(self, driver):
#         super(AppsButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id("Apps")
#
#
# class StatusAppIcon(BaseButton):
#     def __init__(self, driver):
#         super(StatusAppIcon, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector(
#             "//*[@text='Status']")
#
#
# class SendMessageButton(BaseButton):
#     def __init__(self, driver):
#         super(SendMessageButton, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id("send-message-button")
#
#     def click(self):
#         self.find_element().click()
#         self.driver.info('Tap on %s' % self.name)
#
#
# class ConnectionStatusText(BaseText):
#     def __init__(self, driver):
#         super(ConnectionStatusText, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector(
#             "//*[@content-desc='connection-status-text']/android.widget.TextView")
#
#
# class OkContinueButton(BaseButton):
#
#     def __init__(self, driver):
#         super(OkContinueButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='OK, CONTINUE']")
#
#
# class DiscardButton(BaseButton):
#
#     def __init__(self, driver):
#         super(DiscardButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='DISCARD']")
#
#
# class ConfirmButton(BaseButton):
#     def __init__(self, driver):
#         super(ConfirmButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='CONFIRM' or @text='Confirm']")
#
#
# class ProgressBar(BaseElement):
#     def __init__(self, driver, parent_locator: str = ''):
#         super(ProgressBar, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector(parent_locator + '//android.widget.ProgressBar')
#
#
# class CrossIcon(BaseButton):
#     def __init__(self, driver):
#         super(CrossIcon, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector('(//android.view.ViewGroup[@content-desc="icon"])[1]')
#
#
# class NativeCloseButton(BaseButton):
#     def __init__(self, driver):
#         super(NativeCloseButton, self).__init__(driver)
#         self.locator = self.Locator.id('android:id/aerr_close')
#
#
# class CrossIconInWelcomeScreen(BaseButton):
#     def __init__(self, driver):
#         super(CrossIconInWelcomeScreen, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('hide-home-button')
#
#
# class ShowRoots(BaseButton):
#
#     def __init__(self, driver):
#         super(ShowRoots, self).__init__(driver)
#         self.locator = self.Locator.accessibility_id('Show roots')
#
#
# class GetStartedButton(BaseButton):
#
#     def __init__(self, driver):
#         super(GetStartedButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='Get started']")
#
#
# class AssetButton(BaseButton):
#     def __init__(self, driver, asset_name):
#         super(AssetButton, self).__init__(driver)
#         self.asset_name = asset_name
#         self.locator = self.Locator.xpath_selector('(//*[@content-desc=":' + self.asset_name + '-asset-value"])[1]')
#
#     @property
#     def name(self):
#         return self.asset_name + self.__class__.__name__
#
#     def click(self):
#         self.wait_for_element().click()
#         self.driver.info('Tap on %s' % self.name)
#
#
# class OpenInStatusButton(BaseButton):
#     def __init__(self, driver):
#         super(OpenInStatusButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector('//*[@text="Open in Status"]')
#
#     def click(self):
#         self.wait_for_visibility_of_element()
#         # using sleep is wrong, but implicit wait for element can't help in particular case
#         time.sleep(3)
#         self.swipe_to_web_element()
#         self.wait_for_element().click()
#
# class StatusInBackgroundButton(BaseButton):
#     def __init__(self, driver):
#         super(StatusInBackgroundButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector('//*[contains(@content-desc,"Status")]')
#
#
# class EnterQRcodeEditBox(BaseEditBox):
#     def __init__(self, driver):
#         super(EnterQRcodeEditBox, self).__init__(driver)
#         self.locator = self.Locator.text_selector('Message')
#
#     def scan_qr(self, value):
#         self.set_value(value)
#         OkButton(self.driver).click()
#
#
# class OkGotItButton(BaseButton):
#     def __init__(self, driver):
#         super(OkGotItButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@text='Okay, got it']")
#
#     def click(self):
#         self.wait_for_element().click()
#         self.wait_for_invisibility_of_element()
#
#
# class AirplaneModeButton(BaseButton):
#     def __init__(self, driver):
#         super(AirplaneModeButton, self).__init__(driver)
#         self.locator = self.Locator.xpath_selector("//*[@content-desc='Airplane mode']")
#
#     def click(self):
#         self.driver.info('Turning on airplane mode')
#         action = TouchAction(self.driver)
#         action.press(None, 50, 0).move_to(None, 50, 300).perform()
#         super(AirplaneModeButton, self).click()
#         self.driver.press_keycode(4)
#
#
# class SearchInput(BaseEditBox):
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.locator = self.Locator.accessibility_id('search-input')


class BaseView(object):
    def __init__(self, driver):
        self.driver = driver
        # self.send_message_button = SendMessageButton(self.driver)
        # self.home_button = HomeButton(self.driver)
        # self.wallet_button = WalletButton(self.driver)
        # self.profile_button = ProfileButton(self.driver)
        # self.dapp_tab_button = DappTabButton(self.driver)
        # self.status_button = StatusButton(self.driver)
        #
        # self.yes_button = YesButton(self.driver)
        # self.no_button = NoButton(self.driver)
        # self.back_button = BackButton(self.driver)
        # self.allow_button = AllowButton(self.driver)
        # self.deny_button = DenyButton(self.driver)
        # self.continue_button = ContinueButton(self.driver)
        # self.ok_button = OkButton(self.driver)
        self.next_button = BaseButton(self.driver, translation_id = 'next')
        # self.add_button = AddButton(self.driver)
        # self.save_button = SaveButton(self.driver)
        # self.done_button = DoneButton(self.driver)
        # self.delete_button = DeleteButton(self.driver)
        # self.ok_continue_button = OkContinueButton(self.driver)
        # self.discard_button = DiscardButton(self.driver)
        # self.confirm_button = ConfirmButton(self.driver)
        # self.connection_status = ConnectionStatusText(self.driver)
        # self.cross_icon = CrossIcon(self.driver)
        # self.native_close_button = NativeCloseButton(self.driver)
        # self.show_roots_button = ShowRoots(self.driver)
        #self.get_started_button = GetStartedButton(self.driver)

        self.get_started_button = BaseButton(self.driver, xpath = "//*[@text='Get started']")
            #BaseButton(self.driver).Locator.xpath_selector('//*[@text="Get started"]')
        # self.ok_got_it_button = OkGotItButton(self.driver)
        # self.progress_bar = ProgressBar(self.driver)
        # self.cross_icon_iside_welcome_screen_button = CrossIconInWelcomeScreen(self.driver)
        # self.status_in_background_button = StatusInBackgroundButton(self.driver)
        # self.cancel_button = CancelButton(self.driver)
        # self.search_input = SearchInput(self.driver)
        # self.share_button = ShareButton(self.driver)
        #
        # # external browser
        # self.search_in_google_edit_box = SearchEditBox(self.driver)
        # self.open_in_status_button = OpenInStatusButton(self.driver)
        #
        # self.apps_button = AppsButton(self.driver)
        # self.status_app_icon = StatusAppIcon(self.driver)
        #
        # self.airplane_mode_button = AirplaneModeButton(self.driver)
        # self.enter_qr_edit_box = EnterQRcodeEditBox(self.driver)

        self.element_types = {
            'base': BaseElement,
            'button': BaseButton,
            'edit_box': BaseEditBox,
            'text': BaseText
        }

    @property
    def status_account_name(self):
        return self.get_translation_by_key('ethereum-account')

    def accept_agreements(self):
        iterations = int()
        self.close_native_device_dialog("Messages has stopped")
        self.close_native_device_dialog("YouTube")
        while iterations <= 1 and (self.ok_button.is_element_displayed(2) or
                                   self.continue_button.is_element_displayed(2)):
            for button in self.ok_button, self.continue_button:
                try:
                    button.wait_for_element(3)
                    button.click()
                except (NoSuchElementException, TimeoutException):
                    pass
            iterations += 1

    def get_translation_by_key(self, id):
        return transl[id]

    def rooted_device_continue(self):
        try:
            self.continue_button.wait_for_element(3)
            self.continue_button.click()
        except (NoSuchElementException, TimeoutException):
            pass

    def close_native_device_dialog(self, alert_text_part):
        element = self.element_by_text_part(alert_text_part)
        if element.is_element_present(1):
            self.driver.info("Closing '%s' alert..." % alert_text_part)
            self.dismiss_alert()

    def dismiss_alert(self):
        self.native_close_button.click()
        self.driver.info("Alert closed")


    @property
    def logcat(self):
        logcat = self.driver.get_log("logcat")
        if len(logcat) > 1000:
            return str([i for i in logcat if not ('appium' in str(i).lower() or ':1.000000.' in str(i).lower())])
        raise TimeoutError('Logcat is empty')

    def confirm(self):
        self.driver.info("Tap 'Confirm' on native keyboard")
        self.driver.press_keycode(66)

    def confirm_until_presence_of_element(self, desired_element, attempts=3):
        counter = 0
        while not desired_element.is_element_present(1) and counter <= attempts:
            try:
                self.confirm()
                self.driver.info('Wait for %s' % desired_element.name)
                desired_element.wait_for_element(5)
                return
            except TimeoutException:
                counter += 1

    def just_fyi(self, string):
        self.driver.info('=========================================================================')
        self.driver.info(string)

    def click_system_back_button(self, times=1):
        self.driver.info('Click system back button')
        for _ in range(times):
            self.driver.press_keycode(4)

    def put_app_to_background_and_back(self, time_in_background=1):
        self.driver.press_keycode(187)
        time.sleep(time_in_background)
        self.status_in_background_button.click()

    def click_system_home_button(self):
        self.driver.info('Press system Home button')
        self.driver.press_keycode(3)

    def put_app_to_background(self):
        self.driver.info('App to background')
        self.driver.press_keycode(187)

    def cut_text(self):
        self.driver.info('Cut text')
        self.driver.press_keycode(277)

    def copy_text(self):
        self.driver.info('Copy text')
        self.driver.press_keycode(278)

    def paste_text(self):
        self.driver.info('Paste text')
        self.driver.press_keycode(279)

    def send_as_keyevent(self, string):
        keys = {'0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12, '6': 13, '7': 14, '8': 15, '9': 16,

                ',': 55, '-': 69, '+': 81, '.': 56, '/': 76, '\\': 73, ';': 74, ' ': 62,
                '[': 71, ']': 72, '=': 70, '\n': 66, '_': [69, 5], ':': [74, 5],

                'a': 29, 'b': 30, 'c': 31, 'd': 32, 'e': 33, 'f': 34, 'g': 35, 'h': 36, 'i': 37, 'j': 38,
                'k': 39, 'l': 40, 'm': 41, 'n': 42, 'o': 43, 'p': 44, 'q': 45, 'r': 46, 's': 47, 't': 48,
                'u': 49, 'v': 50, 'w': 51, 'x': 52, 'y': 53, 'z': 54}
        time.sleep(3)
        self.driver.info("Enter '%s' using native keyboard" % string)
        for i in string:
            if i.isalpha() and i.isupper():
                keycode, metastate = keys[i.lower()], 64  # META_SHIFT_LEFT_ON Constant Value: 64. Example: i='n' -> 'N'
            elif type(keys[i]) is list:
                keycode, metastate = keys[i][0], keys[i][1]
            else:
                keycode, metastate = keys[i], None
            self.driver.press_keycode(keycode=keycode, metastate=metastate)

    def find_full_text(self, text, wait_time=60):
        self.driver.info("Looking for full text: '%s'" % text)
        element = BaseElement(self.driver)
        element.locator = element.Locator.text_selector(text)
        return element.wait_for_element(wait_time)

    def find_text_part(self, text, wait_time=60):
        self.driver.info("Looking for a text part: '%s'" % text)
        element = BaseElement(self.driver)
        element.locator = element.Locator.text_part_selector(text)
        return element.wait_for_element(wait_time)

    def element_by_text(self, text, element_type='button'):
        self.driver.info("Looking for an element by text: '%s'" % text)
        element = self.element_types[element_type](self.driver)
        element.locator = element.Locator.text_selector(text)
        return element

    def element_by_text_part(self, text, element_type='button'):
        self.driver.info("Looking for an element by text part: '%s'" % text)
        element = self.element_types[element_type](self.driver)
        element.locator = element.Locator.text_part_selector(text)
        return element

    def element_starts_with_text(self, text, element_type='base'):
        self.driver.info("Looking for full text: '%s'" % text)
        element = self.element_types[element_type](self.driver)
        element.locator = element.Locator.xpath_selector("//*[starts-with(@text,'%s')]" % text)
        return element

    def find_element_by_translation_id(self, id, element_type='base', uppercase=False):
        self.driver.info("Looking element by id: '%s'" % id)
        element = self.element_types[element_type](self.driver)
        element.locator = element.Locator.translation_id(id, uppercase=uppercase)
        return element

    def wait_for_element_starts_with_text(self, text, wait_time=60):
        self.driver.info("Looking for element, start with text: '%s'" % text)
        element = BaseElement(self.driver)
        element.locator = element.Locator.xpath_selector("//*[starts-with(@text,'%s')]" % text)
        return element.wait_for_element(wait_time)

    def element_by_accessibility_id(self, accessibility_id, element_type='button'):
        self.driver.info("Looking for an element by accessibility id: '%s'" % accessibility_id)
        element = self.element_types[element_type](self.driver)
        element.locator = element.Locator.accessibility_id(accessibility_id)
        return element

    def element_by_xpath(self, xpath, element_type='button'):
        self.driver.info("Looking for an element by xpath: '%s'" % xpath)
        element = self.element_types[element_type](self.driver)
        element.locator = element.Locator.xpath_selector(xpath)
        return element

    def swipe_up(self):
        size = self.driver.get_window_size()
        self.driver.swipe(size["width"]*0.5, size["height"]*0.8, size["width"]*0.5, size["height"]*0.2)

    def swipe_down(self):
        size = self.driver.get_window_size()
        self.driver.swipe(size["width"]*0.5, size["height"]*0.2, size["width"]*0.5, size["height"]*0.8)

    def swipe_left(self):
        size = self.driver.get_window_size()
        self.driver.swipe(size["width"]*0.8, size["height"]*0.8, size["width"]*0.2, size["height"]*0.8)

    def swipe_right(self):
        size = self.driver.get_window_size()
        self.driver.swipe(size["width"]*0.2, size["height"]*0.8, size["width"]*0.8, size["height"]*0.8)

    def get_status_test_dapp_view(self):
        from views.web_views.status_test_dapp import StatusTestDAppView
        return StatusTestDAppView(self.driver)

    def get_home_view(self):
        from views.home_view import HomeView
        return HomeView(self.driver)

    def get_chat_view(self):
        from views.chat_view import ChatView
        return ChatView(self.driver)

    def get_sign_in_view(self):
        from views.sign_in_view import SignInView
        return SignInView(self.driver)

    def get_send_transaction_view(self):
        from views.send_transaction_view import SendTransactionView
        return SendTransactionView(self.driver)

    def get_base_web_view(self):
        from views.web_views.base_web_view import BaseWebView
        return BaseWebView(self.driver)

    def get_profile_view(self):
        from views.profile_view import ProfileView
        return ProfileView(self.driver)

    def get_wallet_view(self):
        from views.wallet_view import WalletView
        return WalletView(self.driver)

    @staticmethod
    def get_unique_amount():
        return '0.00%s' % datetime.now().strftime('%-d%-H%-M%-S').strip('0')

    @staticmethod
    def get_random_chat_name():
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(7))

    def get_text_from_qr(self):
        image = Image.open(BytesIO(base64.b64decode(self.driver.get_screenshot_as_base64())))
        image.load()
        try:
            return str(zbarlight.scan_codes('qrcode', image)[0])[2:][:132]
        except IndexError:
            raise BaseException('No data in QR code')

    def public_key_to_address(self, public_key):
        raw_public_key = bytearray.fromhex(public_key.replace('0x04', ''))
        return datatypes.PublicKey(raw_public_key).to_address()[2:]

    def get_back_to_home_view(self, times_to_click_on_back_btn=3):
        counter = 0
        while BackButton(self.driver).is_element_displayed(2):
            try:
                if counter >= times_to_click_on_back_btn:
                    break
                self.back_button.click()
                counter += 1
            except (NoSuchElementException, TimeoutException):
                continue
        return self.home_button.click()

    def relogin(self, password=common_password):
        try:
            profile_view = self.profile_button.click()
        except (NoSuchElementException, TimeoutException):
            self.get_back_to_home_view()
            profile_view = self.profile_button.click()
        profile_view.logout()
        sign_in_view = self.get_sign_in_view()
        sign_in_view.sign_in(password)

    def close_share_popup(self):
        TouchAction(self.driver).tap(None, 255, 104, 1).perform()
        time.sleep(3)


    def get_public_key_and_username(self, return_username=False):
        profile_view = self.profile_button.click()
        default_username = profile_view.default_username_text.text
        profile_view.share_my_profile_button.click()
        profile_view.public_key_text.wait_for_visibility_of_element()
        public_key = profile_view.public_key_text.text
        self.click_system_back_button()
        user_data = (public_key, default_username) if return_username else public_key
        return user_data

    def share_via_messenger(self):
        self.element_by_text_part("Direct share").wait_for_element()
        self.element_by_text('Messages').click()
        self.element_by_text('New message').click()
        self.send_as_keyevent('+0100100101')
        self.confirm()

    def click_upon_push_notification_by_text(self, text):
        self.element_by_text_part(text).click()
        return self.get_chat_view()

    def reconnect(self):
        connect_status = self.connection_status
        for i in range(3):
            if connect_status.is_element_displayed(5, ignored_exceptions=StaleElementReferenceException):
                if 'Tap to reconnect' in connect_status.text:
                    try:
                        connect_status.click()
                    except AttributeError:
                        pass
                    try:
                        connect_status.wait_for_invisibility_of_element()
                    except TimeoutException as e:
                        if i == 2:
                            e.msg = "Device %s: Can't reconnect to mail server after 3 attempts" % self.driver.number
                            raise e

    def find_values_in_logcat(self, **kwargs):
        logcat = self.logcat
        items_in_logcat = list()
        for key, value in kwargs.items():
            if re.findall(r'\W%s$|\W%s\W' % (value, value), logcat):
                items_in_logcat.append('%s in logcat!!!' % key.capitalize())
        return items_in_logcat

    def find_values_in_geth(self, *args):
        b64_log = self.driver.pull_file(geth_log_emulator_path)
        file = base64.b64decode(b64_log)
        result = False
        for value in args:
            self.driver.info('Checking for %s entry' % value)
            if re.findall('%s*' % value, file.decode("utf-8")):
                self.driver.info('%s was found in geth.log' % value)
                result = True
        return result


    def asset_by_name(self, asset_name):
        return AssetButton(self.driver, asset_name)

    def open_notification_bar(self):
        self.driver.open_notifications()

    def toggle_airplane_mode(self):
        self.airplane_mode_button.click()
        self.close_native_device_dialog("MmsService")

    def toggle_mobile_data(self):
        self.driver.start_activity(app_package='com.android.settings', app_activity='.Settings')
        network_and_internet = self.element_by_text('Network & internet')
        network_and_internet.wait_for_visibility_of_element()
        network_and_internet.click()
        toggle = self.element_by_accessibility_id('Wi‑Fi')
        toggle.wait_for_visibility_of_element()
        toggle.click()
        self.driver.back()
        self.driver.back()

    def open_universal_web_link(self, deep_link):
        start_web_browser(self.driver)
        self.driver.info('Open %s web link via web browser' % deep_link)
        self.driver.get(deep_link)

    def upgrade_app(self):
        self.driver.install_app(pytest_config_global['apk_upgrade'], replace=True)
        self.driver.info('Upgrading apk to apk_upgrade')

    def search_by_keyword(self, keyword):
        self.driver.info('Search for %s' % keyword)
        self.search_input.click()
        self.search_input.send_keys(keyword)

    # Method-helper
    def write_page_source_to_file(self, full_path_to_file):
        string_source = self.driver.page_source
        source = open(full_path_to_file, "a+")
        source.write(string_source)

