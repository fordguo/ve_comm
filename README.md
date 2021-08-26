# Virtual Meeting Common Library


## settings 配置

### 微信相关

- WECHAT_APPID
- WECHAT_SID
- WECHAT_SHARE_DEBUG  
- WECHAT_SIGNATURE_URL
- WECHAT_H5_URL
- WECHAT_DEFAULT_LINK

- WECHAT_UCP_KEY
- WECHAT_UCP_URL
- WECHAT_TEMPLATES

### Matomo网页嵌码

- MATOMO_HOST
- MATOMO_SITE_ID
- MATOMO_URL
- MATOMO_CONTAINER

## 注意事项

### 直播

#### 直播URL

1. 匿名用户获取不到直播间的个性化，必须登录以后，才能再次获取到用户相关的URL。

## 国际化

目前默认支持简体中文、繁体中文和英文

- 创建/更新PO文件
`python manage.py makemessages -l en -l zh_Hans -l zh_Hant`
- 编译PO文件
`python manage.py compilemessages`
