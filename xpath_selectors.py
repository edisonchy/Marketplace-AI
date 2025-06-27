def build_class_condition(classes):
    return " and ".join([f"contains(@class, '{cls}')" for cls in classes])

def unread_badge_xpath():
    classes = ['D_lm', 'D_ln', 'D_lr', 'D_lu', 'D_lx', 'D_l_', 'D_arx', 'D_lJ']
    return f'//span[{build_class_condition(classes)} and string(number(normalize-space(text()))) != "NaN"]'

def message_xpath():
    classes = ['D_lm', 'D_ln', 'D_ls', 'D_lq', 'D_lu', 'D_lx', 'D_lz', 'D_ctB', 'D_cts', 'D_lH']
    return f'//div[starts-with(@id, "chat-message-")]//p[{build_class_condition(classes)}]'

def product_xpath():
    classes = ["D_lm", "D_ln", "D_lr", "D_lt", "D_lx", "D_lz", "D_bhy", "D_lH"]
    return f"//p[{build_class_condition(classes)}]"

def text_area_xpath():
    return "//textarea[@placeholder='Type here...']"

def send_button_xpath():
    return "//button[.//div[text()='Send']]"