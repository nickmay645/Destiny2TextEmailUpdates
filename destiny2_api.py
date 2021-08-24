from selenium import webdriver
import sms
import smtplib
from email.message import EmailMessage

vendor_scan_list = ["ADA-1", "BANSHEE-44"]
info_list = ["MATERIAL EXCHANGE"]


def email_alert(subject, body, to):
    # 160 char max

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "destiny2smsupdates@gmail.com"
    password = ""
    msg['from'] = user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


if __name__ == '__main__':

    url = 'https://www.todayindestiny.com/vendors'
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    vendors = driver.find_elements_by_class_name('vendorCardContainer')
    for vendor in vendors:
        message = ""
        name = vendor.find_element_by_class_name('vendorCardHeaderName')
        if name.text in vendor_scan_list:
            print("\n" + name.text)
            message += "\n" + name.text
            groups = vendor.find_elements_by_class_name('vendorCategoryContainer')
            for group in groups:
                group_text = group.text.replace("► ", "")
                if group_text == "MATERIAL EXCHANGE:":
                    items = group.find_elements_by_class_name('vendorInventoryItemContainer')
                    for item in items[0:2]:
                        itemTooltipContainer = item.find_element_by_class_name("itemTooltipContainer")
                        itemTooltipHeaderContainer = itemTooltipContainer.find_element_by_class_name(
                            "itemTooltipHeaderContainer")
                        itemName = itemTooltipHeaderContainer.find_element_by_class_name('itemTooltip_itemName')
                        itemType = itemTooltipHeaderContainer.find_element_by_class_name('itemTooltip_itemType')
                        print(itemName.get_attribute('textContent'), itemType.get_attribute('textContent'))
                        message += "\n" + itemName.get_attribute('textContent') + " | " + itemType.get_attribute(
                            'textContent')

            email_alert("Mods", message, "3307013905@messaging.sprintpcs.com")
