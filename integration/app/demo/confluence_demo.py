import json
from atlassian import Confluence

confluence = Confluence(url="https://confluence.zhito.com:8090",
                        username="wangshiyuan",
                        password="zhito26@#")
# confluence.login()
print(confluence)

config = {
    "project": "GSL4_X86",
    "version": "1.1",
    "build_type": "Debug",
    "base": {
        "message_group": {
            "url": "git@gitlab.zhito.com:ai/message_group.git",
            "version": "feature/zhito_l4_cicd"
        },
        "common": {
            "url": "git@gitlab.zhito.com:ai/zhito_common.git",
            "version": "feature/zhito_l4_cicd"
        },
        "map": {
            "url": "git@gitlab.zhito.com:ai/map_module.git",
            "version": "feature/zhito_l4_cicd"
        },
        "zlam_common": {
            "url": "git@gitlab.zhito.com:zlam/zlam_common.git",
            "version": "feature/zhito_l4_cicd"
        },
        "perception_common": {
            "url": "git@gitlab.zhito.com:ai/perception_common.git",
            "version": "feature/zhito_l4_cicd"
        }
    },
    "modules": {
        "drivers": {
            "url": "git@gitlab.zhito.com:drivers/drivers.git",
            "version": "feature/zhito_l4_cicd"
        }
    }
}

space = "ITD"
title = "page6"
pre = '<p class="auto-cursor-target">本次构建配置信息如下：</p><p class="auto-cursor-target"><br /></p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="06dba324-f02c-4410-8fa5-190d5d7f8bcd"><ac:plain-text-body><![CDATA['
suf = '}]]></ac:plain-text-body></ac:structured-macro><p><br /></p>'
content = pre + json.dumps(config, indent=4) + suf
parent_page = {"id": 56111727}

# new_page = confluence.create_page(space=space, title=title, body=content, parent_id=parent_page['id'])
# print("\n\npage:\n", new_page["_links"]["webui"])
# print("\n\nnew_page:", new_page)

# print("\n\nnew_page.id:", new_page["id"])
# page = confluence.get_page_by_id(new_page["id"])
# print("\n\npage:", page)
# print("New page created: " + confluence.get_page_url(new_page['id']))

page = confluence.get_page_by_title(space=space,
                                    title="GSL4_X86【应用】")
# print("\n\npage:\n", page["_links"]["webui"])
if page == None:
    print("Not Found!")
print("\n", page)

# print("\n\npage:\n", page["body"]["storage"]["value"])

# import requests
# import json # loads / dumps

# headers = {
#     'Content-Type': 'application/json',
# }
# response = requests.get(
#     'https://confluence.zhito.com:8090/rest/api/space/ITD',
#     headers=headers,
#     auth=("wangshiyuan", "zhito26@#"))
# print(response, response.text)

# response = requests.get(
#     'https://confluence.zhito.com:8090/rest/api/content/56102841',
#     headers=headers,
#     auth=("wangshiyuan", "zhito26@#"))
# print("\n\n", response, response.text) # _links.webui

# 1. Install the Atlassian Python API library (called "atlassian-python-api") using pip.

# ```
# pip install atlassian-python-api
# ```

# 2. Create an instance of the Confluence class from the API.

# ```python
# from atlassian import Confluence

# confluence = Confluence(
#     url='https://your-confluence-url.com/',
#     username='your-username',
#     password='your-password'
# )
# ```

# 3. Use the `create_page()` function to create a new page in Confluence.

# ```python
# result = confluence.create_page(
#     space = 'your-space-key',
#     title = 'Your Page Title',
#     body = 'Your page content in Confluence Storage Format (CSF), e.g. <p>This is some text</p>',
#     parent_id = 12345678  # ID of the parent page (optional)
# )
# ```

# 4. If you want to update an existing page, use the `update_page()` function instead.

# ```python
# result = confluence.update_page(
#     page_id = 12345678,
#     title = 'Your Updated Page Title',
#     body = 'Your updated page content in CSF'
# )
# ```

# 5. To delete a page, use the `delete_page()` function.

# ```python
# confluence.delete_page(page_id=12345678)
# ```

# That's it! With these few lines of Python code, you can start creating and updating pages in Confluence. Remember to format your page content in Confluence Storage Format (CSF) to ensure correct rendering of elements like headings, bullet points, and tables.