const error = {

    /* 前端字符串检验错误 */

    /* 注册、修改个人信息 */
    emptyUsername: 'Please input your username',
    incorrectUsername: '16 characters or less, cannot include "@"',

    /* 注册、找回密码 */
    emptyEmail: 'Please input your email',
    incorrectEmail: 'Please input correct email',

    /* 登录 */
    emptyUsernameOrEmail: 'Please input your username or email',
    incorrectUsernameOrEmail: 'Please input correct username or email',

    /* 注册、登录、找回密码、修改密码 */
    emptyPassword: 'Please input your password',
    incorrectPassword: 'Letters / numbers / English punctuation, Length 8-32',

    /* 注册、找回密码 */
    emptyCheckPassword: 'Please input your password again',
    incorrectCheckPassword: 'The two entered passwords are inconsistent',

    /* 修改密码 */
    emptyOldPassword: 'Please input your old password',
    emptyNewPassword: 'Please input your new password',
    emptyCheckNewPassword: 'Please input your new password again',
    incorrectCheckNewPassword: 'The two entered new passwords are inconsistent',

    /* 注册，找回密码 */
    emptyCode: 'Please input your code',
    incorrectCode: 'Verification code is 4 digits',

};


export default error
