const Settings = () => import(/* webpackChunkName: "setting" */ './Settings.vue')
const ProfileSetting = () => import(/* webpackChunkName: "setting" */ './children/ProfileSetting.vue')
const SecuritySetting = () => import(/* webpackChunkName: "setting" */ './children/SecuritySetting.vue')
const AccountSetting = () => import(/* webpackChunkName: "setting" */ './children/AccountSetting.vue')
const MyPage = () => import(/* webpackChunkName: "setting" */ './children/MyPage.vue')
const AccountArticleList = () => import('./children/AccountArticleList.vue')

export {Settings, ProfileSetting, SecuritySetting, AccountSetting, MyPage, AccountArticleList}
